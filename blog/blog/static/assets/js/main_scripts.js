function addToFavorite(url, slug, element) {
    $.ajax({
        url: url,
        type: "get",
        data : {
            "slug": slug
        },
        success: function (data, textStatus, response) {
            if (response.responseJSON) {
                if (data.state === "added") {
                    if ($(element).hasClass("btn-primary")) {
                    }
                    else{
                        $(element).addClass("btn-primary")
                    }
                }
                else {
                    $(element).removeClass("btn-primary")
                }
            }
//            else{
//
//                let popoverTriggerList = [].slice.call(document.querySelector(`[id="${String(element.id)}"`))
//                let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
//                return new bootstrap.Popover(popoverTriggerEl)})
//                $(`[id="${String(element.id)}"]`).popover({html:true})
//                $(`[id="${String(element.id)}"]`).popover("show")
//            }
        },
        error: function(response, textStatus, errorThrown) {
            alert("Sign in to add to favorite any post");
            console.log(response)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })

}
