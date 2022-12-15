# %%

a = 56+56
# %%

# you cane name also strings

name = "marcello"
surname = 'marchesi'

fullname = name + " " + surname
fullname
# %%
age = 420

# you can do couples or triples, or n-uples more generally tuples
marcello = (fullname, age)
gianni = ("gianni", 69)

# you cin do list of things (arrays, vectors, lists)
tizi = [marcello, gianni, ('carlo',43), ('mario', 23)] 
tizi[0][0]


# create a tizio object with name and age
#%%
tizio = {'name': 'tizio', 'age': 23}
tizio['name']
#list of tizi
tizi = [tizio, {'name': 'caio', 'age': 24}, {'name': 'sempronio', 'age': 25}, tizio]

#%%
for tizio in tizi:
    print(tizio['name'], tizio['age'])
    if (tizio['age'] > 24 or tizio['name'] == 'caio'):
        print('the previous is caio or older than 23')
        
    

# %%
