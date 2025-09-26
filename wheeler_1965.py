import sympy as sp

class Wheller_1965:
    def __init__(self, er, h, freq):
        self.er = er      # relative permittivity
        self.h = h        # height of substrate (m)
        self.freq = freq  # frequency in GHz

    def Analyze(self, w, l):
        Z0 = self.__calculate_Z0(w)
        L = self.__calculate_elec_length(w, l)
        return float(Z0), float(L)

    def Synthesize(self, Z0_target, elec_length_target):
        # Define symbols
        w, l = sp.symbols("w l", positive=True, real=True)

        # Effective permittivity expression (symbolic in terms of w)
        Eeff = ((self.er + 1) / 2) + ((self.er - 1) / 2) * (1 + 12 * (self.h / w))**-0.5

        # Characteristic impedance expression
        U = w / self.h
        Z0_expr = sp.Piecewise(
            (
                (60 / sp.sqrt(Eeff)) * sp.log((8 / U) + (U / 4)),
                U <= 3.3
            ),
            (
                (120 * sp.pi) / (sp.sqrt(Eeff) * (U + 1.393 + 0.667 * sp.log(U + 1.444))),
                True
            )
        )

        # Electrical length expression
        c = 2.99792458e8
        f_hz = self.freq * 1e9
        lambda_g = c / (f_hz * sp.sqrt(Eeff))
        theta_expr = (360 * l) / lambda_g

        # Solve system of equations
        solutions = sp.nsolve(
            [
                Z0_expr - Z0_target,
                theta_expr - elec_length_target
            ],
            [w, l],
            [self.h, 0.03]  # initial guess (w ~ h, l ~ 3cm)
        )

        return float(solutions[0]), float(solutions[1])

    def __calculate_Z0(self, w):
        U = w / self.h
        Eeff = self.__calculate_eff(w)

        if U <= 3.3:
            z0 = (60 / sp.sqrt(Eeff)) * sp.log((8 / U) + (U / 4))
        else:
            z0 = (120 * sp.pi) / (sp.sqrt(Eeff) * (U + 1.393 + 0.667 * sp.log(U + 1.444)))

        return z0

    def __calculate_elec_length(self, w, L):
        c = 2.99792458e8
        f_hz = self.freq * 1e9
        Eeff = self.__calculate_eff(w)

        lambda_g = c / (f_hz * sp.sqrt(Eeff))
        theta_deg = (360 * L) / lambda_g
        return theta_deg

    def __calculate_eff(self, w):
        return ((self.er + 1) / 2) + ((self.er - 1) / 2) * (1 + 12 * (self.h / w))**-0.5


if __name__ == "__main__":
    w = Wheller_1965(er=4.4, h=1.6e-3, freq=2.4)  # FR4 substrate
    # Z0, L = w.Analyze(w=4e-5, l=30e-3)
    # print("Analyze:")
    # print("Z0 = {:.2f} Ω".format(Z0))
    # print("Electrical length = {:.2f}°".format(L))

    w_calc, l_calc = w.Synthesize(207.67, 144.09)
    print("\nSynthesize:")
    print("Width = {:.6f} m".format(w_calc))
    print("Length = {:.6f} m".format(l_calc))
