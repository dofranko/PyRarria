L = [3,8,4,1,1]
P = 32
c = 4
W = 10
sub_L = []
suma = 0

X=2*P


def divice(List, start):
    global suma
    j = 0
    S = 0
    end = start - 1
    for i in List[start:]:
        end += 1
        S += (i * j * c)
        if i*c == P:
            sub_L.append(L[start:end])
            sub_L.append([end])
            return end+1
        elif S > X and end == len(L)-1:
            suma += (S - (i * j))
            sub_L.append(L[start:end])
            sub_L.append(L[end:end + 1])
            return end

        elif S > X:
            suma += (S - (i * j))
            sub_L.append(L[start:end])
            return end

        elif end == len(L) - 1:
            sub_L.append(L[start:end + 1])
            suma+=S
            return end


        j += 1

koniec = 0
while koniec != len(L) - 1:
    koniec = divice(L, koniec)

print("Podkolejki zamówień: "+str(sub_L))
counter = 0
for i in sub_L:
    print("zamów " + str(sum(i)) + " paczek dnia " + str(counter))
    counter += len(i)
print("koszt magazynowania to: "+str(suma)+ "*" +str(c)+ ", koszt zamówienia to " + str(len(sub_L))+"*"+str(P))
print("Łączny koszt to: "+str((suma*c)+len(sub_L)*P))
