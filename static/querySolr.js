$(document).ready(function() {

    $.ajax({
        url: "http://localhost:8983/solr/dico/query",
        data: {
            'q': searchText, // Texte saisi
            'wt': "json", // Modèle linguistique
            'rows': 10,
            'start': 0
        },
        success: function(response) {
            $(".reponse-bloc").empty();
            console.log("Réponse de l'API :", response);
            $(".reponse-bloc").append("<div class='reponse-wrapper'><h2 id='reponse-api-title'>Résultat(s)</h2></div>");
            $(".reponse-wrapper").append("<pre>"+extractText(response['response'])+"</pre>");
        },
        error: function(xhr, status, error) {
            console.error("Erreur lors de la requête AJAX : ", error);
        },
    });


    function extractText(SearchOutput) {
        if (!SearchOutput['numFoundExact']==true)
        {
            return "Rien n'est trouvé.";
        }
        var DataFormated = "<div class='results-container'>";
        for (let doc of SearchOutput["docs"]) {
            let id = doc['id'];
            let lemme = doc['lemme'];
            let pos = doc['pos'].join(", ");
            let def = doc['def'].join("<br>");
            let synonymes = doc['synonyme'].join(", ");

            DataFormated += "<div class='result-item'>";
            DataFormated += "<h3 class='result-id'>ID : " + id + "</h3>";
            DataFormated += "<p><strong>LEMME : </strong>" + lemme + "</p>";
            DataFormated += "<p><strong>POS : </strong>" + pos + "</p>";
            DataFormated += "<p><strong>Définition(s) :</strong><br>" + def + "</p>";
            DataFormated += "<p><strong>Synonymes :</strong> " + synonymes + "</p>";
            DataFormated += "</div><hr>";
        }
        DataFormated += "</div>";
        
        return DataFormated;
    }
});