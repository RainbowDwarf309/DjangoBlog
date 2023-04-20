function updatePostViews(url, code_id, action) {
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
                if (data.state === "viewed") {
                    post_views = document.getElementById("views")
                    post_views.innerHTML = '<i class="ti-eye"></i> Views: ' + data.views
                }
            }
        },
        error: function(response, textStatus, errorThrown) {
            alert("");
            console.log(response)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })
}


function addToFavorite(url, slug, element) {
    let host = window.location.protocol + "//" + window.location.host
    $.ajax({
        url: host + url,
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
            else{
                $('#heart').popover({
                placement: 'right',
                content: "Only authorized users can add posts to their favorites. Please sign in!",
                trigger: 'hover'
                })
            }
        },
        error: function(response, textStatus, errorThrown) {
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
            else{
                $('#like-post').popover({
                placement: 'right',
                content: "Only authorized users can set likes to posts. Please sign in!",
                trigger: 'hover'
                })
                $('#dislike-post').popover({
                placement: 'right',
                content: "Only authorized users can set dislikes to posts. Please sign in!",
                trigger: 'hover'
                })
            }
        },
        error: function(response, textStatus, errorThrown) {
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
            else{
                $('#comment-like-' + code_id).popover({
                placement: 'right',
                content: "Only authorized users can set likes to comments. Please sign in!",
                trigger: 'hover'
                })
                $('#comment-dislike-' + code_id).popover({
                placement: 'right',
                content: "Only authorized users can set dislikes to comments. Please sign in!",
                trigger: 'hover'
                })
            }
        },
        error: function(response, textStatus, errorThrown) {
            console.log(response)
            console.log(textStatus)
            console.log(errorThrown)
        }
    })
}

function changeNewsletterForm(element_id) {
  const changedElement = document.getElementById(element_id).value;
  document.getElementById("newsletter-save").disabled = false;
}
