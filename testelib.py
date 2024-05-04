import nanovna as vna

a = vna.Nvna(3)#Versão no NanoVNA: V2 vai de 50KHz-3GHz, V3 vai de 1MHz-6GHz 
a.measure(1000000000,1000000000,2,1)#valores usados no excel, na mesma ordem
a.close()
""" Em construção
[f1,s11] = a.extract("S11")
[f2,s21] = a.extract("S21")
"""