# Store Sales Annalysis

[PJS3 2019-2020 Mission2.pdf](Store%20Sales%20Annalysis/PJS3_2019-2020_Mission2.pdf)

## **Résumé du Projet :**

Nous avons été fourni des fichiers CSV représentants des données d'un magasin sur les mois de Juin, Juillet, et Août. Chacun de ces fichiers représentent des tables de données comme par exemple : "Catégorie", "Carte de Fidélité", Produit" etc.. Nous devrons grâce à ses données répondre à plusieurs requêtes :

- Evolution mensuelle du chiffre d’affaire du magasin
- Evolution mensuelle du prix moyen des tickets de caisse
- Evolution mensuelle du chiffre d’affaire des catégories de produits suivantes :

    a. Produits Vegan
    b. Produits Bio
    c. Produits Hallal
    d. Produits Casher

- Le prix moyen des tickets de caisse par client
- Les clients qui achètent des produits des catégories suivantes et leurs dépenses
mensuelles associées :

    a. Produits Vegan
    b. Produits Bio
    c. Produits Hallal
    d. Produits Casher

## Requète 1 : Evolution mensuelle du chiffre d’affaire du magasin :

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.41.48.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.41.48.png)

    ### REQUETE1 ###
    ticketAvecDetail = ticket.set_index("NoTicket").join(detailTicket.set_index("NoTicket"))
    ticketAvecDetail["Total"] = (ticketAvecDetail.PrixUnit * ticketAvecDetail.Qte) * (1 - ticketAvecDetail.Remise)
    chiffreAffaireMois = ticketAvecDetail.resample('M', on="DateTicket").Total.sum()

**Constat :**

On remarque une baisse du CA au mois d'Août par rapport au mois de Juillet.

## Requète 2 : Evolution mensuelle du prix moyen des tickets de caisse :

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.41.59.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.41.59.png)

    ### REQUETE2 ###
    prixMoyenMois = ticketAvecDetail.resample('M', on="DateTicket").Total.mean()

**Constat :**

On remarque que le prix moyen des tickets de caisses à légérement baissé en Août alors qu'on a vue une grande baisse du chiffre d'affaire dans le graphe au-dessus. Ceci est logique vue que le chiffre d'affaire prends en compte le nombre de ventes qui était nettement supérieur en Juillet alors que la moyenne ne prend pas en compte ce paramètre.

## Requète 3 : Evolution mensuelle du chiffre d’affaire des catégories de produits suivantes  :

a. Produits Vegan
b. Produits Bio
c. Produits Hallal
d. Produits Casher

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.12.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.12.png)
```python
    ### REQUETE3 ###
    detailProduit = ticketAvecDetail.set_index("Refprod").join(produit.set_index("Refprod"))
    produitsMois = {}
    for t in types:
    	detailProduit[t] = detailProduit["Nomprod"].str.contains(t + "|" + t.lower() + "|" + t.upper(), na=False)
    	temp = detailProduit.drop(detailProduit[detailProduit[t]==False].index, inplace=False)
    	produitsMois[t] = temp.resample('M',on="DateTicket").Total.sum()
```
**Constat :**

Nous nous rendons compte que nos clients consomment tous pour la majorité des produits bios. 

## Requète 4 : Le prix moyen des tickets de caisse par client  :

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.37.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.37.png)
```python
    ### REQUETE4 ###
    ticket = ticket.set_index("NoTicket")
    ticket["Total"] = ticketAvecDetail.groupby("NoTicket").Total.mean()
    ticketClient = carteFidelite.set_index("CodeCli").join(ticketAvecDetail.set_index("CodeCli"))
    carteFidelite = carteFidelite.set_index("CodeCli")
    prixMoyenClient = ticketClient.groupby("CodeCli").Total.mean()
    prixMoyenClient = prixMoyenClient.sort_values()
```
**Constat :**

Grâce à cette représentation graphique nous pouvons savoir quel client a déboursé le plus en moyenne sur la totalité des deux mois. 

## Requète 5 : Les clients qui achètent des produits des catégories suivantes et leurs dépenses mensuelles associées :
```python
    ### REQUETE5 ###
    clientsProduits = {}
    for t in types:
    	detailProduit[t] = detailProduit["Nomprod"].str.contains(t + "|" + t.lower() + "|" + t.upper(), na=False)
    	temp = detailProduit.drop(detailProduit[detailProduit[t]==False].index, inplace=False)
    	temp["Mois"] = pandas.DatetimeIndex(temp["DateTicket"]).month
    	clientsProduits[t] = temp.groupby(["CodeCli", "Mois"]).Total.sum()
    # R5
    for i in ["Vegan", "Bio", "Halal", "Casher"]:
    	clientsProduits[i].unstack().plot.bar(stacked=True)
    	plt.subplots_adjust(top=0.95,left=0.05,bottom=0.15,right=0.98)
    	plt.title("Dépenses en produits "+i+" par clients par mois")
    	plt.xlabel("Client")
    	plt.ylabel("Dépense en €")
    	plt.show()
```
a. Produits Vegan

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.53.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.42.53.png)

b. Produits Bio

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.43.06.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.43.06.png)

c.Produits Hallal

![Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.43.22.png](Store%20Sales%20Annalysis/Screen_Shot_2020-02-06_at_21.43.22.png)

d.Produits Casher