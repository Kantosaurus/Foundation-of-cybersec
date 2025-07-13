# 50.042 FCS Lab 5 Modular Arithmetic
# Year 2025

import copy
class Polynomial2:
    def __init__(self,coeffs):
        # Store coefficients as a list, where index i represents coefficient of x^i
        # Remove trailing zeros to normalize the polynomial
        self.coeffs = coeffs[:]  # Make a copy to avoid modifying the input
        self._normalize()
    
    def _normalize(self):
        """Remove trailing zeros to normalize the polynomial"""
        while len(self.coeffs) > 1 and self.coeffs[-1] == 0:
            self.coeffs.pop()
    
    def degree(self):
        """Return the degree of the polynomial"""
        return len(self.coeffs) - 1
    
    def add(self,p2):
        # Polynomial addition in GF(2) is XOR operation
        max_len = max(len(self.coeffs), len(p2.coeffs))
        result = []
        for i in range(max_len):
            a = self.coeffs[i] if i < len(self.coeffs) else 0
            b = p2.coeffs[i] if i < len(p2.coeffs) else 0
            result.append(a ^ b)  # XOR in GF(2)
        return Polynomial2(result)

    def sub(self,p2):
        return self.add(p2)

    def mul(self,p2,modp=None):
        if modp is None:
            result_len = len(self.coeffs) + len(p2.coeffs) - 1
            result = [0] * result_len
            
            for i in range(len(self.coeffs)):
                for j in range(len(p2.coeffs)):
                    if self.coeffs[i] == 1 and p2.coeffs[j] == 1:
                        result[i + j] ^= 1  # XOR in GF(2)
            
            return Polynomial2(result)
        else:
            temp_result = self.mul(p2)
            return temp_result.div(modp)[1]

    def div(self,p2):
        if len(p2.coeffs) == 1 and p2.coeffs[0] == 0:
            raise ValueError("Division by zero polynomial")
        
        dividend = self.coeffs[:]
        divisor = p2.coeffs[:]
        divisor_degree = len(divisor) - 1
        
        quotient = [0] * max(1, len(dividend) - divisor_degree)
        remainder = dividend[:]
        
        for i in range(len(dividend) - divisor_degree, -1, -1):
            if i + divisor_degree < len(remainder) and remainder[i + divisor_degree] == 1:
                quotient[i] = 1
                for j in range(len(divisor)):
                    if i + j < len(remainder):
                        remainder[i + j] ^= divisor[j]
        
        return Polynomial2(quotient), Polynomial2(remainder)

    def __str__(self):
        if len(self.coeffs) == 1 and self.coeffs[0] == 0:
            return "0"
        
        terms = []
        for i in range(len(self.coeffs)):
            if self.coeffs[i] == 1:
                if i == 0:
                    terms.append("1")
                elif i == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{i}")
        
        if not terms:
            return "0"
        
        return " + ".join(reversed(terms))

    def getInt(self):
        result = 0
        for i, coeff in enumerate(self.coeffs):
            if coeff == 1:
                result |= (1 << i)
        return result

    @staticmethod
    def getIntStatic(p):
        return p.getInt()


class GF2N:
    affinemat=[[1,0,0,0,1,1,1,1],
               [1,1,0,0,0,1,1,1],
               [1,1,1,0,0,0,1,1],
               [1,1,1,1,0,0,0,1],
               [1,1,1,1,1,0,0,0],
               [0,1,1,1,1,1,0,0],
               [0,0,1,1,1,1,1,0],
               [0,0,0,1,1,1,1,1]]

    def __init__(self,x,n=8,ip=Polynomial2([1,1,0,1,1,0,0,0,1])):
        self.n = n
        self.ip = ip
        
        if isinstance(x, int):
            coeffs = []
            for i in range(n):
                coeffs.append((x >> i) & 1)
            self.p = Polynomial2(coeffs)
        else:
            if isinstance(x, Polynomial2):
                coeffs = x.coeffs[:n]
                while len(coeffs) < n:
                    coeffs.append(0)
                self.p = Polynomial2(coeffs)
            else:
                raise ValueError("x must be an integer or Polynomial2")

    def add(self,g2):
        result_poly = self.p.add(g2.p)
        result_coeffs = result_poly.coeffs[:self.n]
        while len(result_coeffs) < self.n:
            result_coeffs.append(0)
        return GF2N(Polynomial2(result_coeffs), self.n, self.ip)

    def sub(self,g2):
        return self.add(g2)
    
    def mul(self,g2):
        result_poly = self.p.mul(g2.p, self.ip)
        return GF2N(result_poly, self.n, self.ip)

    def div(self,g2):
        q, r = self.p.div(g2.p)
        return GF2N(q, self.n, self.ip), GF2N(r, self.n, self.ip)

    def getPolynomial2(self):
        return self.p

    def __str__(self):
        return str(self.getInt())

    def getInt(self):
        return self.p.getInt()

    def mulInv(self):
        
        if self.p.coeffs == [0]:
            return GF2N(0, self.n, self.ip)
        r1 = self.ip
        r2 = self.p
        t1 = Polynomial2([0])
        t2 = Polynomial2([1])
        
        while r2.coeffs != [0]:
            q, r = r1.div(r2)
            r_new = r1.add(q.mul(r2))
            r1 = r2
            r2 = r_new
            t_new = t1.add(q.mul(t2))
            t1 = t2
            t2 = t_new
        
        if r1.coeffs == [1]:
            result_coeffs = t1.coeffs[:self.n]
            while len(result_coeffs) < self.n:
                result_coeffs.append(0)
            return GF2N(Polynomial2(result_coeffs), self.n, self.ip)
        else:
            raise ValueError("Multiplicative inverse does not exist")

    def affineMap(self):
        input_val = self.getInt()
        vector = [0] * 8
        for i in range(8):
            vector[7-i] = (input_val >> i) & 1  # MSB first
        
        result = [0] * 8
        b = [1, 1, 0, 0, 0, 1, 1, 0]  # 0x63 in binary (MSB first)
        
        for i in range(8):
            sum_val = 0
            for j in range(8):
                sum_val ^= (self.affinemat[i][j] & vector[j])
            result[i] = sum_val ^ b[i]
        
        result_val = 0
        for i in range(8):
            result_val |= (result[7-i] << i)
        
        return GF2N(result_val, self.n, self.ip)

print('\nTest 1')
print('======')
print('p1=x^5+x^2+x')
print('p2=x^3+x^2+1')
p1=Polynomial2([0,1,1,0,0,1])
p2=Polynomial2([1,0,1,1])
p3=p1.add(p2)
print('p3= p1+p2 = ',p3)

print('\nTest 2')
print('======')
print('p4=x^7+x^4+x^3+x^2+x')
print('modp=x^8+x^7+x^5+x^4+1')
p4=Polynomial2([0,1,1,1,1,0,0,1])
# modp=Polynomial2([1,1,0,1,1,0,0,0,1])
modp=Polynomial2([1,0,0,0,1,1,0,1,1])
p5=p1.mul(p4,modp)
print('p5=p1*p4 mod (modp)=',p5)

print('\nTest 3')
print('======')
print('p6=x^12+x^7+x^2')
print('p7=x^8+x^4+x^3+x+1')
p6=Polynomial2([0,0,1,0,0,0,0,1,0,0,0,0,1])    
p7=Polynomial2([1,1,0,1,1,0,0,0,1])
p8q,p8r=p6.div(p7)
print('q for p6/p7=',p8q)
print('r for p6/p7=',p8r)

####
print('\nTest 4')
print('======')
g1=GF2N(100)
g2=GF2N(5)
print('g1 = ',g1.getPolynomial2())
print('g2 = ',g2.getPolynomial2())
g3=g1.add(g2)
print('g1+g2 = ',g3)

print('\nTest 5')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g4=GF2N(0b1101,4,ip)
g5=GF2N(0b110,4,ip)
print('g4 = ',g4.getPolynomial2())
print('g5 = ',g5.getPolynomial2())
g6=g4.mul(g5)
print('g4 x g5 = ',g6.p)

print('\nTest 6')
print('======')
# Create a default irreducible polynomial for 13-bit field
ip_13 = Polynomial2([1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])  # x^13 + 1
g7=GF2N(0b1000010000100,13,ip_13)
g8=GF2N(0b100011011,13,ip_13)
print('g7 = ',g7.getPolynomial2())
print('g8 = ',g8.getPolynomial2())
q,r=g7.div(g8)
print('g7/g8 =')
print('q = ',q.getPolynomial2())
print('r = ',r.getPolynomial2())

print('\nTest 7')
print('======')
ip=Polynomial2([1,1,0,0,1])
print('irreducible polynomial',ip)
g9=GF2N(0b101,4,ip)
print('g9 = ',g9.getPolynomial2())
print('inverse of g9 =',g9.mulInv().getPolynomial2())

print('\nTest 8')
print('======')
ip=Polynomial2([1,1,0,1,1,0,0,0,1])
print('irreducible polynomial',ip)
g10=GF2N(0xc2,8,ip)
print('g10 = 0xc2')
g11=g10.mulInv()
print('inverse of g10 = g11 =', hex(g11.getInt()))
g12=g11.affineMap()
print('affine map of g11 =',hex(g12.getInt()))
