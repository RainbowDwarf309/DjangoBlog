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

function setPostLikeOrDislike(url, slug, action, element) {
    $.ajax({
        url: url,
        type: "get",
        data : {
            "slug": slug,
            "action": action
        },
        dataType: "json",
        success: function (data, textStatus, response) {
            if (response.responseJSON) {
                if (data.state === "like") {
                    post_rate = document.getElementById("rating")
                    post_rate.innerHTML = data.rate
                }
                else if(data.state === "dislike") {
                    post_rate = document.getElementById("rating")
                    post_rate.innerHTML = data.rate
                }
            }
        },
        error: function(response, textStatus, errorThrown) {
            alert("Sign in to set like or dislike");
            console.log(response)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })
}


function setCommentLikeOrDislike(url, code_id, action, element) {
    $.ajax({
        url: url,
        type: "get",
        data : {
            "code_id": code_id,
            "action": action
        },
        dataType: "json",
        success: function (data, textStatus, response) {
            if (response.responseJSON) {
                if (data.state === "like") {
                    post_rate = document.getElementById("rating-" + code_id)
                    post_rate.innerHTML = data.rate
                }
                else if(data.state === "dislike") {
                    post_rate = document.getElementById("rating-" + code_id)
                    post_rate.innerHTML = data.rate
                }
            }
        },
        error: function(response, textStatus, errorThrown) {
            alert("Sign in to set like or dislike");
            console.log(response)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })
}
