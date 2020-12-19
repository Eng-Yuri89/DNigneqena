(function ($) {
    "use strict";
    $("#basicScenario").jsGrid({
        width: "100%",
        filtering: true,
        editing: true,
        inserting: true,
        sorting: true,
        paging: true,
        autoload: true,
        loadIndication: true,
        loadMessage: 'Loading transactions...',
        pActionSize: 15,
        pActionButtonCount: 5,
        deleteConfirm: "Do you really want to delete the client?",
        noDataContent: 'No Transactions',
        controller: {
             loadData: function (filter) {
            return $.ajax({
                method: 'GET',
                url: '/api/v2/category/',
                dataType: 'json',
                headers: {
                    'X-CSRF-TOKEN': $('#token').val()
                },
                data: filter
            });
        },


            insertItem: function (item) {
                return $.ajax({
                    type: "POST",
                    url: "/api/v2/category/",
                    dataType: 'json',
                headers: {
                    'X-CSRF-TOKEN': $('#token').val()
                },
                    data: item
                });
            },

            updateItem: function (item) {
                return $.ajax({
                    type: "PUT",
                    url: "/api/v2/category/" + item.id,
                    dataType: 'json',
                headers: {
                    'X-CSRF-TOKEN': $('#token').val()
                },
                    data: item
                });
            },

            deleteItem: function (item) {
                return $.ajax({
                    type: "DELETE",
                    url: "/api/v2/category/" + item.id

                });
            }
        },
        fields: [
            {
                name: "image",
                itemTemplate: function (val, item) {
                    return $("<img>").attr("src", val).addClass("blur-up lazyloaded").css({
                        height: 50,
                        width: 50
                    }).on("click", function () {
                        $("#imagePreview").attr("src", item.Img);
                        $("#dialog").dialog("open");
                    });
                },
                insertTemplate: function () {
                    var insertControl = this.insertControl = $("<input>").prop("type", "file");
                    return insertControl;
                },
                insertValue: function () {
                    return this.insertControl[0].files[0];
                },
                align: "center",
                width: 50
            },
            {name: "title", type: "text", width: 100 , align: 'center'},
            {name: "slug", type: "text", width: 50},
            {name: "keywords", type: "text", width: 50},
            {name: "description", type: "text", width: 50},
            {type: "control"}
        ]
    });
})(jQuery);
