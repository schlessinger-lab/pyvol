
from .spheres import Spheres
import numpy as np
import scipy
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize


def cluster_within_r(spheres, radius, allow_new=True):
    r_indices = np.where(spheres.r == radius)[0]
    selected = spheres.xyzrg[r_indices, :]
    
    ungrouped_indices = np.where(selected[:, 4] == 0)[0]

    if ungrouped_indices.shape[0] > 0:
        ungrouped_data = selected[ungrouped_indices]
        db = DBSCAN(eps=radius, min_samples=1).fit(ungrouped_data[:, 0:3])

        if allow_new:
            starting_index = np.amax(selected[:, 4]) + 1
            np.put(spheres.g, r_indices[ungrouped_indices], db.labels_ + starting_index)
        else:
            starting_index = np.amin(selected[:, 4]) - 1
            np.put(spheres.g, r_indices[ungrouped_indices], -1 * db.labels_ + starting_index)


def cluster_between_r(spheres, ref_radius, target_radius):
    ref_data = spheres.xyzrg[spheres.r == ref_radius]
    r_indices = np.where(spheres.r == target_radius)[0]
    target_data = spheres.xyzrg[r_indices]

    if (ref_data.shape[0] > 0) and (target_data.shape[0] > 0):

        kdtree = scipy.spatial.cKDTree(ref_data[:, 0:3])
        dist, indices = kdtree.query(target_data[:, 0:3], distance_upper_bound=ref_radius, n_jobs=-1)
        
        target_indices = indices < ref_data.shape[0]
        ref_indices = indices[target_indices]

        np.put(spheres.g, r_indices[target_indices], ref_data[ref_indices, 4])

        
def cluster_improperly_grouped(spheres, radius, min_cluster_size=1, max_clusters=None):
    min_group = np.amin(spheres.g)
    group_list = np.flip(np.arange(min_group, 0), axis=0)
    reassign_groups_to_closest(spheres, group_list, radius)

    spheres.remove_ungrouped()

    group_counts = np.bincount(spheres.g.astype(int))
    small_groups = np.where(group_counts < min_cluster_size)
    reassign_groups_to_closest(spheres, small_groups, radius)

    group_counts = np.bincount(spheres.g.astype(int))
    num_groups = np.count_nonzero(group_counts)

    if max_clusters is not None:
        if num_groups > max_clusters:
            reassign_groups_to_closest(spheres, np.where(group_counts > 0)[0], radius, iterations=(num_groups - max_clusters))


def extract_groups(spheres, surf_radius=None):
    groups = np.unique(spheres.g)

    group_list = []
    for group in groups:
        group_spheres = Spheres(xyzrg = spheres.xyzrg[spheres.g == group].copy())
        group_list.append(group_spheres)

    if surf_radius is not None:
        exterior_list = [group_spheres.calculate_surface(probe_radius=surf_radius)[0] for group_spheres in group_list]
        reindices = np.flip(np.argsort([s.mesh.volume for s in exterior_list]))

        new_group_list = []
        new_ext_list = []
        for index in reindices:
            g_s = group_list[index]
            e_s = exterior_list[index]

            g_s.g = index
            e_s.g = index
            g_s.mesh = e_s.mesh.copy()
            new_group_list.append(g_s)
            new_ext_list.append(e_s)

        return new_group_list
    else:
        return group_list
    

def hierarchically_cluster_spheres(spheres, ordered_radii=None, min_new_radius=None, min_cluster_size=10, max_clusters=None):
    if min_new_radius is None:
        min_new_radius = np.amin(ordered_radii)
    
    for index, radius in enumerate(ordered_radii):
        initial_grouped = spheres.xyzrg[spheres.g != 0].shape[0]
        if index > 0:
            cluster_between_r(spheres, ref_radius=ordered_radii[index - 1], target_radius=ordered_radii[index])
            
        cluster_within_r(spheres, radius, allow_new=(radius >= min_new_radius))

    cluster_improperly_grouped(spheres, radius=ordered_radii[-1], min_cluster_size=min_cluster_size, max_clusters=max_clusters)
    
    
def identify_closest_grouped(spheres, group, radius):
    target_indices = np.where((spheres.r == radius) & (spheres.g == group))[0]
    grouped_indices = np.where((spheres.r == radius) & (spheres.g > 0) & (spheres.g != group))[0]
        
    target_data = spheres.xyzrg[target_indices]
    grouped_data = spheres.xyzrg[grouped_indices]

    if (target_data.shape[0] > 0) and (grouped_data.shape[0] > 0):
        kdtree = scipy.spatial.cKDTree(grouped_data[:, 0:3])
        dist, indices = kdtree.query(target_data[:, 0:3], distance_upper_bound=1.41 * radius, n_jobs=-1)
        # 1.41 factor allows the two spheres to intersect at pi/4 from the closest point
        
        t_indices = indices < grouped_data.shape[0]
        group_indices = indices[t_indices]
        if len(group_indices) > 0:
            counts = np.bincount(grouped_data[group_indices,4].astype(int))
            closest = np.argmax(counts)
            magnitude = counts[closest]
            return [group, closest, magnitude]
        else:            
            return [None, None, 0]
    else:
        return [None, None, 0]


def merge_sphere_list(s_list, r=None, g=None):
    selected_data_list = []

    for i, s in enumerate(s_list):
        if s is None:
            continue
        selected_data = s.xyzrg

        if r is not None:
            selected_data = selected_data[selected_data[:, 3] == r]
        if g is not None:
            selected_data = selected_data[selected_data[:, 4] == g]

        if selected_data.shape[0] > 0:
            selected_data_list.append(selected_data)

    if len(selected_data_list) > 0:
        return Spheres(xyzrg=np.vstack(selected_data_list))
    else:
        return None


def reassign_group(spheres, source_group, target_group):
    source_indices = np.where(spheres.g == source_group)

    np.put(spheres.g, source_indices, target_group)
    

def reassign_groups_to_closest(spheres, group_list, radius, iterations=None, preserve_largest=False):
    if iterations is None:
        iterations = len(group_list)
    
    for i in range(iterations):
        linkages = []
        for group in group_list:
            linkages.append(identify_closest_grouped(spheres, group, radius))

        nonzero_linkages = [link for link in linkages if link[2] > 0]
        if len(nonzero_linkages) > 0:
            best_link = sorted(nonzero_linkages, key=lambda x: x[2])[-1]
            if preserve_largest:
                group_sizes = np.bincount(spheres.g.astype(int))
                if group_sizes[best_link[0]] > group_sizes[best_link[1]]:
                    best_link = [best_link[1], best_link[0]]
            
            reassign_group(spheres, best_link[0], best_link[1])
        else:
            break


def remove_interior(spheres):
    min_rad = np.amin(spheres.r)
    max_rad = np.amax(spheres.r)

    point_tree = scipy.spatial.cKDTree(spheres.xyz)
    neighbors = point_tree.query_ball_tree(point_tree, r=(max_rad - min_rad))

    interior_indices = []
    for point_index, nlist in enumerate(neighbors):
        if point_index in interior_indices:
            continue
        
        if len(nlist) <= 1:
            continue
        
        inclusion = spheres.r[point_index] - spheres.r[nlist].reshape(-1, 1) - scipy.spatial.distance.cdist(spheres.xyz[nlist], spheres.xyz[point_index].reshape(1, -1))
        included_indices = np.where(inclusion > 0)[0]
        if len(included_indices) > 0:
            interior_indices.extend(list(np.array(nlist)[included_indices]))
    
    interior_indices = np.unique(interior_indices).astype(int)
    spheres.xyzrg = np.delete(spheres.xyzrg, interior_indices, axis=0)
    

def remove_overlap(spheres, radii=None, spacing=0.1, iterations=20, tolerance=0.02):
    groups = np.unique(spheres.g)[:-1]
    
    if radii is None:
        radii = [np.amax(spheres.r)]
        spacing = radii[0]

    for radius in radii:
        for group in groups:
            group_indices = np.where((spheres.g == group) & (spheres.r > (radius - spacing)) & (spheres.r <= radius))[0]
            other_indices = np.where((spheres.g != group) & (spheres.r > (radius - spacing)) & (spheres.r <= radius))[0]


            if len(group_indices) == 0 or len(other_indices) == 0:
                continue

            group_data = spheres.xyzrg[group_indices]
            other_data = spheres.xyzrg[other_indices]
        
            other_tree = scipy.spatial.cKDTree(other_data[:, 0:3])
            group_tree = scipy.spatial.cKDTree(group_data[:, 0:3])

            neighbors = group_tree.query_ball_tree(other_tree, r=2 * radius)

            altered_group_indices = []
            altered_other_indices = []

            for iteration in range(iterations):
                overlaps = np.zeros(len(neighbors))
                overlap_indices = -1 * np.ones(len(neighbors))
            
                for group_index, nlist in enumerate(neighbors):
                    if len(nlist) == 0:
                        continue
                    overlap = other_data[nlist, 3].reshape(-1, 1) + group_data[group_index, 3] - scipy.spatial.distance.cdist(other_data[nlist, 0:3], group_data[group_index, 0:3].reshape(1, -1))
                    most_overlapping_index = np.argmax(overlap)
                    if overlap[most_overlapping_index] > 0:
                        overlaps[group_index] = overlap[most_overlapping_index]
                        overlap_indices[group_index] = nlist[most_overlapping_index]

                overlapped_group_indices = np.where(overlaps > tolerance)[0]
                if len(overlapped_group_indices) == 0:
                    break
                
                overlaps = overlaps[overlapped_group_indices]
                overlap_indices = overlap_indices[overlapped_group_indices].astype(int)
            
                reorder = np.argsort(overlaps)[::-1]
                overlaps = overlaps[reorder]
                overlap_indices = overlap_indices[reorder]
                overlapped_group_indices = overlapped_group_indices[reorder]

                foo, closest_indices = np.unique(overlap_indices, return_index=True)
                overlaps = overlaps[closest_indices]
                overlap_indices = overlap_indices[closest_indices]
                overlapped_group_indices = overlapped_group_indices[closest_indices]

                overlap_adjustment = 0.25 * overlaps
                vector = overlap_adjustment[:, np.newaxis] * normalize(group_data[overlapped_group_indices, 0:3] - other_data[overlap_indices, 0:3])

                group_data[overlapped_group_indices, 0:3] = group_data[overlapped_group_indices, 0:3] + vector
                group_data[overlapped_group_indices, 3] = group_data[overlapped_group_indices, 3] - overlap_adjustment

                other_data[overlap_indices, 0:3] = other_data[overlap_indices, 0:3] - vector
                other_data[overlap_indices, 3] = other_data[overlap_indices, 3] - overlap_adjustment

                altered_group_indices.extend(list(overlapped_group_indices))
                altered_other_indices.extend(list(overlap_indices))

            altered_group_indices = np.unique(altered_group_indices).astype(int)
            altered_other_indices = np.unique(altered_other_indices).astype(int)

            spheres.xyzrg[group_indices[altered_group_indices]] = group_data[altered_group_indices]
            spheres.xyzrg[other_indices[altered_other_indices]] = other_data[altered_other_indices]
