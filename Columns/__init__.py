import os, sys
# for initial setting doesnt remove
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas

bwl=[]
hl=[]
hfl=[]
bl=[]
name_l=[]
mass_l=[]
weight_l=[]

for bw in range(25,65,5):
    for h in range(40,155,5):
        for hf in [15,17,20,25]:
            for tabla in [0,1]:
                bwl.append(bw)
                hl.append(h)
                hfl.append(hf)
                if tabla == 0:
                    b=bw+6*hf
                    bl.append(b)
                    name_l.append('B'+str(bw)+'/'+str(h)+'/T'+str(hf))
                    mass_l.append(1-(hf*b)/(hf*b+bw*(h-hf)))
                    weight_l.append(1-(hf*b)/(hf*b+bw*(h-hf)))
                    
                else:
                    b=bw+2.25*hf
                    bl.append(b)
                    name_l.append('B'+str(bw)+'/'+str(h)+'/Y'+str(hf))
                    mass_l.append(1-(hf*b)/(hf*b+bw*(h-hf)))
                    weight_l.append(1-(hf*b)/(hf*b+bw*(h-hf)))


data={}
data['name']=name_l
data['h']=hl
data['b']=bl
data['hf']=hfl
data['bw']=bwl
data['mass_modifier']=mass_l
data['weight_modifier']=weight_l


dataframe = pandas.DataFrame(data)


print(dataframe)