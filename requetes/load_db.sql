SELECT nom_produit, description, note, evaluation, prix, tblprix.monnaie, status_produit, date_creation, date_maj FROM amatable
INNER JOIN tblprix ON amatable.keyzon = tblprix.keyzon
WHERE date_maj=(SELECT MAX(date_maj) FROM tblprix
WHERE amatable.keyzon = tblprix.keyzon)
ORDER by amatable.keyzon;