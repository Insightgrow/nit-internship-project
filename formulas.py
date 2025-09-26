import math

class Formulas:

    def __init__(self, er, h, t=0.0):
        if not all(isinstance(i, (int, float)) for i in [er, h, t]) or er <= 0 or h <= 0 or t < 0:
            raise ValueError("Dielectric constant (er) and height (h) must be positive. Thickness (t) must be non-negative.")
        self.er = er
        self.h = h
        self.t = t

    def analyze(self, w, formula='hammerstad_jensen_1980'):
        if formula == 'hammerstad_jensen_1980':
            return self._analyze_hammerstad_jensen_1980(w)
        elif formula == 'wheeler_1977':
            return self._analyze_wheeler_1977(w)
        elif formula == 'schneider_1969':
            return self._analyze_schneider_1969(w)
        elif formula == 'hammerstad_1975':
            return self._analyze_hammerstad_1975(w)
        elif formula == 'wheeler_1965':
            return self._analyze_wheeler_1965(w)
        else:
            raise ValueError(f"Unknown formula: {formula}")

    def synthesize(self, z0, formula='hammerstad_jensen_1980'):
        if formula == 'hammerstad_jensen_1980':
            return self._synthesize_hammerstad_jensen_1980(z0)
        elif formula in ['wheeler_1977', 'schneider_1969', 'hammerstad_1975', 'wheeler_1965']:
             return self._synthesize_standard(z0)
        else:
            raise ValueError(f"Unknown formula: {formula}")

    def _get_effective_width(self, w):
        if self.t > 0:
            return w + (self.t / math.pi) * (1 + math.log(2 * self.h / self.t))
        return w
    
    def _analyze_hammerstad_jensen_1980(self, w):
        w_eff = self._get_effective_width(w)
        u = w_eff / self.h
        a = 1 + (1/49)*math.log((u**4 + (u/52)**2)/(u**4 + 0.432)) + (1/18.7)*math.log(1 + (u/18.1)**3)
        b = 0.564 * ((self.er - 0.9)/(self.er + 3))**0.053
        e_eff = (self.er + 1)/2 + ((self.er - 1)/2) * (1 + 10/u)**(-a*b)
        f_u = 6 + (2*math.pi - 6) * math.exp(-(30.666/u)**0.7528)
        z0 = (376.73 / (2 * math.pi * math.sqrt(e_eff))) * math.log(f_u/u + math.sqrt(1 + (2/u)**2))
        return z0, e_eff

    def _synthesize_hammerstad_jensen_1980(self, z0):
        A = math.exp((z0 * math.sqrt(self.er + 1)) / 42.4 - ((self.er - 1)/(self.er + 1)) * (0.23 + 0.11/self.er))
        w_over_h_provisional = 8 * math.exp(A) / (math.exp(2*A) - 2)
        if w_over_h_provisional < 2:
            w_h = w_over_h_provisional
        else:
            B = (377 * math.pi) / (2 * z0 * math.sqrt(self.er))
            w_h = (2/math.pi) * (B - 1 - math.log(2*B - 1) + ((self.er - 1) / (2 * self.er)) * (math.log(B - 1) + 0.39 - (0.61/self.er)))
        
        if self.t > 0:
            delta_w_t = self.t/math.pi * math.log(1 + (4 * math.exp(1))/( (self.t/self.h) * math.cosh(math.sqrt((w_h*2*math.pi)**2))))
            return w_h * self.h - delta_w_t
        return w_h * self.h
    
    def _synthesize_standard(self, z0):
        A = (z0/60) * math.sqrt((self.er+1)/2) + ((self.er-1)/(self.er+1))*(0.23 + 0.11/self.er)
        B = (377*math.pi)/(2*z0*math.sqrt(self.er))
        w_over_h_provisional = (8*math.exp(A)) / (math.exp(2*A)-2)
        if w_over_h_provisional <= 2:
            w_h = w_over_h_provisional
        else:
            w_h = (2/math.pi) * (B - 1 - math.log(2*B-1) + ((self.er-1)/(2*self.er)) * (math.log(B-1) + 0.39 - (0.61/self.er)))
        return w_h * self.h
        
    def _analyze_wheeler_1977(self, w):
        w_eff = self._get_effective_width(w)
        x = w_eff / self.h
        m = 1 + (4*math.pi*x)/(x+1) * (14+8/x**2)/(7+4/x**2)
        z0_air = (42.4 / math.sqrt(x+1)) * math.log(m)
        e_eff = (self.er + 1)/2 + ((self.er - 1)/2) * (1 + 10/x)**-0.5
        z0 = z0_air / math.sqrt(e_eff)
        return z0, e_eff
    
    def _analyze_schneider_1969(self, w):
        u = w / self.h
        e_eff = (self.er + 1)/2 + ((self.er - 1)/2) * (1 / math.sqrt(1 + 10/u))
        if u <= 1:
            z0 = (60 / math.sqrt(e_eff)) * math.log(8/u + u/4)
        else:
            z0 = (120 * math.pi / math.sqrt(e_eff)) / (u + 2.42 - 0.44/u + (1-1/u)**6)
        return z0, e_eff
    
    def _analyze_hammerstad_1975(self, w):
        u = w / self.h
        e_eff = (self.er + 1)/2 + ((self.er-1)/2) * (1/math.sqrt(1 + 12/u))
        if u <= 1:
            z0 = (60 / math.sqrt(e_eff)) * math.log(8/u + u/4)
        else:
            z0 = (120 * math.pi / math.sqrt(e_eff)) / (u + 1.393 + 0.667*math.log(u+1.444))
        return z0, e_eff

    def _analyze_wheeler_1965(self, w):
        u = w / self.h
        e_eff = (self.er+1)/2 + ((self.er-1)/2) * (1/math.sqrt(1+12/u))
        if u <= 1:
            z0 = (60/math.sqrt(e_eff)) * math.log(8/u + u/4)
        else:
            z0 = (120*math.pi/math.sqrt(e_eff)) / (u + 2.42 - 0.44/u + (1-1/u)**6)
        return z0, e_eff

def calculate_physical_length(calc_instance, electrical_length_deg, freq_ghz, w, formula='hammerstad_jensen_1980'):
    c = 299792458000.0  
    _, e_eff = calc_instance.analyze(w, formula=formula)
    lambda_g = c / (freq_ghz * 1e9 * math.sqrt(e_eff))
    return (electrical_length_deg / 360.0) * lambda_g

def calculate_electrical_length(calc_instance, physical_length_mm, freq_ghz, w, formula='hammerstad_jensen_1980'):
    c = 299792458000.0
    _, e_eff = calc_instance.analyze(w, formula=formula)
    lambda_g = c / (freq_ghz * 1e9 * math.sqrt(e_eff))
    return (physical_length_mm / lambda_g) * 360.0

if __name__ == '__main__':
    er_substrate = 4.2
    h_substrate = 1.6  
    t_copper = 0.035  
    calculator = Formulas(er=er_substrate, h=h_substrate, t=t_copper)
    print(f"--- Comparing Analysis Formulas for a Width of 3.0 mm ---\n")
    
    formulas_to_test = [
        'hammerstad_jensen_1980',
        'wheeler_1977',
        'hammerstad_1975',
        'schneider_1969',
        'wheeler_1965'
    ]
    
    for formula_name in formulas_to_test:
        try:
            z0, e_eff = calculator.analyze(w=3.0, formula=formula_name)
            print(f"Formula: {formula_name}")
            print(f"  - Z₀: {z0:.2f} Ohms,  ε_eff: {e_eff:.2f}")
        except Exception as e:
            print(f"Could not calculate for {formula_name}: {e}")

    print(f"\n--- Running Synthesis to get a 50 Ohm line ---\n")
    required_width = abs(calculator.synthesize(z0=50.0, formula='hammerstad_jensen_1980'))
    print(f"To get 50 Ohms using 'hammerstad_jensen_1980' synthesis:")
    print(f"  - Required Width (W): {required_width:.3f} mm")