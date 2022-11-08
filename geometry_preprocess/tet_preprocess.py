import numpy as np


def extract_surface_faces(tet_indices: np.ndarray):
  raw_tet_faces = []
  tet_count = tet_indices.shape[0]

  for i in range(tet_count):
    p1, p2, p3, p4 = np.sort(tet_indices[i])
    raw_tet_faces.append([p1, p2, p3])
    raw_tet_faces.append([p1, p2, p4])
    raw_tet_faces.append([p1, p3, p4])
    raw_tet_faces.append([p2, p3, p4])
  tet_faces = np.array(raw_tet_faces, dtype=int)
  tet_faces = tet_faces[np.lexsort(
      (tet_faces[:, 0], tet_faces[:, 1], tet_faces[:, 2]))]
  assert tet_faces.shape == (tet_count * 4, 3)

  surface_faces_list = []
  i = 0
  while i < tet_faces.shape[0]:
    j = i + 1
    while j < tet_faces.shape[0] and (tet_faces[j] == tet_faces[i]).all():
      j += 1
    if j == i + 1:
      surface_faces_list.append(i)
    i = j

  return tet_faces[surface_faces_list]


def compute_vertex_mass(vert_pos: np.ndarray, tet_indices: np.ndarray):
  vert_mass = np.zeros(shape=vert_pos.shape[0], dtype=float)
  vert_order = np.zeros(shape=vert_pos.shape[0], dtype=int)
  tet_mass = np.zeros(shape=tet_indices.shape[0], dtype=float)
  for i in range(tet_indices.shape[0]):
    p1, p2, p3, p4 = tet_indices[i]
    x1, x2, x3, x4 = vert_pos[[p1, p2, p3, p4]]
    tet_mass[i] = np.abs(np.dot(np.cross(x2 - x1, x3 - x1), (x4 - x1))) / 6.0
    vert_mass[[p1, p2, p3, p4]] += tet_mass[i] / 4.0
    vert_order[[p1, p2, p3, p4]] += 1
  return vert_order, vert_mass, tet_mass
