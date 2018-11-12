(function($) {
  (function() {

    var db = {

        loadData: function(filter) {
            return $.grep(this.clients, function(client) {
                return (!filter.Name || client.Name.indexOf(filter.Name) > -1)
                    && (filter.Age === undefined || client.Age === filter.Age)
                    && (!filter.Address || client.Address.indexOf(filter.Address) > -1)
                    && (!filter.Country || client.Country === filter.Country)
                    && (filter.Married === undefined || client.Married === filter.Married);
            });
        },

        insertItem: function(insertingClient) {
            this.clients.push(insertingClient);
        },

        updateItem: function(updatingClient) { },

        deleteItem: function(deletingClient) {
            var clientIndex = $.inArray(deletingClient, this.clients);
            this.clients.splice(clientIndex, 1);
        }

    };

    window.db = db;


    db.semester = [
        { Name: "", Id: 0 },
        { Name: "1", Id: 1 },
        { Name: "2", Id: 2 },
        { Name: "3", Id: 3 },
        { Name: "4", Id: 4 },
        { Name: "5", Id: 5 },
        { Name: "6", Id: 6 },
        { Name: "7", Id: 7 },
        { Name: "8", Id: 8 },
    ];
    db.section = [
        { Name: "", Id: 0 },
        { Name: "A", Id: 1 },
        { Name: "B", Id: 2 },
        { Name: "C", Id: 3 },
        { Name: "D", Id: 4 },
        { Name: "E", Id: 5 },
        { Name: "F", Id: 6 },
        { Name: "G", Id: 7 },
        { Name: "H", Id: 8 }

    ];
    db.clients = [
        {
            "USN":"01FB15ECS343",
            "Name":"Gracie",
            "Semester":"3",
            "Section":"A",
            "Email":"vas1232@gmail.com"
            
        },
        {
            "USN":"01FB15ECS343",
            "Name":"Gracie",
            "Semester":"3",
            "Section":"A",
            "Email":"vas1232@gmail.com"
            
        }
       
     ];

}());
})(jQuery);
