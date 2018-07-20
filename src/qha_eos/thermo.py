from qha.type_aliases import Matrix, Vector

def static_thermodynamic_potentials(v_vector: Vector, free_energies: Matrix, p_tv: Matrix):
    """
    Calculate :math:`H`, :math:`U`, and :math:`G` on :math:`(T,V)` grid from :math:`F`;

    :math:`U = F + TS, H = U + PV, G = F + PV`

    input: nt, and F, which is Helmholtz Free Energy, are needed.


    :param free_energies: :math:`F(T,V)`
    :param p_tv: pressure, :math:`P(T,V)`
    :param ts: temperature vector
    :param v_vector: fine volumes vector
    :return: :math:`U`, :math:`H`, :math:`G` on :math:`(T,V)` grid
    """
    g: Matrix = free_energies + p_tv * v_vector  # G(T,V) = F(T,V) + V * P(T,V)

    u: Matrix = free_energies  # U(T,V) = F(T,V) + 0 * S(T,V)

    h: Matrix = u + p_tv * v_vector  # H(T,V) = U(T,V) + V * P(T,V)

    return {'U': u, 'H': h, 'G': g}
