import pandas 
import matplotlib.pyplot as plt

pandas.set_option('display.max_columns', None)

# Constantes
carteFidelitePath 	= "Data-30-09-19-20191008T100933Z-001/CarteFidelite.csv"
categoriePath 		= "Data-30-09-19-20191008T100933Z-001/Categorie.csv"
detailTicketPath 	= "Data-30-09-19-20191008T100933Z-001/detailTicket.csv"
produitPath 		= "Data-30-09-19-20191008T100933Z-001/Produit.csv"
ticketPath 			= "Data-30-09-19-20191008T100933Z-001/Ticket.csv"
detailTicketJAPath 	= "7-10 Tickets de Juillet Aout 2019/detailTicketJuilletAout2019.csv"
ticketJAPath 		= "7-10 Tickets de Juillet Aout 2019/TicketJuilletAout2019.csv"
d = ";"
types = ["Vegan", "Bio", "Halal", "Casher"]


# Lecture des CSV
carteFidelite 	= pandas.read_csv(carteFidelitePath,delimiter=d)
categorie 		= pandas.read_csv(categoriePath,delimiter=d)
detailTicket 	= pandas.read_csv(detailTicketPath,delimiter=d)
produit 		= pandas.read_csv(produitPath,delimiter=d)
ticket 			= pandas.read_csv(ticketPath,delimiter=d)
detailTicketJA 	= pandas.read_csv(detailTicketJAPath,delimiter=d)
ticketJA 		= pandas.read_csv(ticketJAPath,delimiter=d)


# Assemblage des tables Juin Juillet Aout
ticket = pandas.concat([ticket,ticketJA])
detailTicket = pandas.concat([detailTicket, detailTicketJA])


# On change le type de 'DateTicket' en type 'datetime'
ticket['DateTicket'] = pandas.to_datetime(ticket['DateTicket'], dayfirst=True)


# On enlève tous les ' €' 
detailTicket['PrixUnit'] = detailTicket['PrixUnit'].str.replace(' €','',case=False) 

# Et on remplace tous les ',' par des '.' pour convertir en string la colonne
detailTicket['PrixUnit'] = detailTicket['PrixUnit'].str.replace(',','.',case=False).astype(float)
detailTicket['Remise'] = detailTicket['Remise'].str.replace(',','.',case=False).astype(float)

# On enlève la colonne "PrixUnit" de Produit pour éviter les conflits
produit.drop(['PrixUnit'],axis='columns',inplace=True)


### REQUETE1 ###
ticketAvecDetail = ticket.set_index("NoTicket").join(detailTicket.set_index("NoTicket"))
ticketAvecDetail["Total"] = (ticketAvecDetail.PrixUnit * ticketAvecDetail.Qte) * (1 - ticketAvecDetail.Remise)
chiffreAffaireMois = ticketAvecDetail.resample('M', on="DateTicket").Total.sum() 

### REQUETE2 ###
prixMoyenMois = ticketAvecDetail.resample('M', on="DateTicket").Total.mean()

### REQUETE3 ###
detailProduit = ticketAvecDetail.set_index("Refprod").join(produit.set_index("Refprod"))
produitsMois = {}
for t in types:
	detailProduit[t] = detailProduit["Nomprod"].str.contains(t + "|" + t.lower() + "|" + t.upper(), na=False)
	temp = detailProduit.drop(detailProduit[detailProduit[t]==False].index, inplace=False)
	produitsMois[t] = temp.resample('M',on="DateTicket").Total.sum()

### REQUETE4 ###
ticket = ticket.set_index("NoTicket")
ticket["Total"] = ticketAvecDetail.groupby("NoTicket").Total.mean()
ticketClient = carteFidelite.set_index("CodeCli").join(ticketAvecDetail.set_index("CodeCli"))
carteFidelite = carteFidelite.set_index("CodeCli")
prixMoyenClient = ticketClient.groupby("CodeCli").Total.mean()
prixMoyenClient = prixMoyenClient.sort_values()

### REQUETE5 ###
clientsProduits = {}
for t in types:
	detailProduit[t] = detailProduit["Nomprod"].str.contains(t + "|" + t.lower() + "|" + t.upper(), na=False)
	temp = detailProduit.drop(detailProduit[detailProduit[t]==False].index, inplace=False)
	temp["Mois"] = pandas.DatetimeIndex(temp["DateTicket"]).month
	clientsProduits[t] = temp.groupby(["CodeCli", "Mois"]).Total.sum()

### AFFICHAGE DES RESULTATS

# R1
chiffreAffaireMois.plot()
plt.title("Chiffre d'affaires par mois")
plt.xlabel("Mois")
plt.ylabel("CA en €")
plt.show()

# R2
prixMoyenMois.plot()
plt.title("Prix moyen d'un ticket de caisse par mois")
plt.xlabel("Mois")
plt.ylabel("Prix moyen en €")
plt.show()

# R3
tousProduits = pandas.concat([produitsMois["Vegan"], produitsMois["Bio"], produitsMois["Halal"], produitsMois["Casher"]], axis='columns')
tousProduits.index = tousProduits.index.month.astype(str)
tousProduits.columns = types
tousProduits.plot(kind='bar')
plt.title("Evolution mensuelle du chiffre d'affaire des catégories de produits")
plt.xlabel('Mois (2019)')
plt.ylabel("Chiffre d'affaire des catégories de produits")
plt.show()


# R4
prixMoyenClient.plot(kind='bar')
plt.subplots_adjust(top=0.95,left=0.05,bottom=0.15,right=0.98)
plt.title("Prix moyen d'un ticket de caisse par client")
plt.xlabel("Client")
plt.ylabel("Prix moyen en €")
plt.show()

# R5
for i in ["Vegan", "Bio", "Halal", "Casher"]:
	clientsProduits[i].unstack().plot.bar(stacked=True)
	plt.subplots_adjust(top=0.95,left=0.05,bottom=0.15,right=0.98)
	plt.title("Dépenses en produits "+i+" par clients par mois")
	plt.xlabel("Client")
	plt.ylabel("Dépense en €")
	plt.show()