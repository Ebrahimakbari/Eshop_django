function ArticleCommentSend(articleID) {
    var parentID = $('#parent_id').val();
    var comment = $('#commenttext').val();
    $.get('/article/comment-add', {
        "comment": comment,
        "article_id": articleID,
        "parent_id": parentID
    }).then(res => {
        $('#comments_area').html(res);
        $('#commenttext').val('');
        $('#parent_id').val("");
        if (parentID !== null && parentID !== "") {
            document.getElementById('single_comment_box_'+parentID).scrollIntoView({behavior: "smooth",block: "start"});
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth",block: "start"});
        }
    });
}


function GetParent(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth",block: "start"});
}

function FilterForm(){
    const price_range = $('#sl2').val();
    const min_price = price_range.split(',')[0];
    const max_price = price_range.split(',')[1];
    $('#min_price').val(min_price);
    $('#max_price').val(max_price);
    $('#price_form').submit();
}

function PageNumberFilterPrice(page){
    $('#page_number').val(page);
    $('#price_form').submit();

}

function showLargeImage(source){
    $('#main_image').attr('src',source);
    $('#image_large').attr('href',source);
}

function addToOrder(productId){
    const productCount = $('#product_count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res =>{
        Swal.fire({
            title: "اعلان",
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: "#3085d6",
            confirmButtonText: res.confirmText
            }).then((result) => {
            if (result.isConfirmed && res.status === 'is not authenticated') {
                window.location.href='/login';
                };
            });
    });
}

function send_count(operation , productId){
    message = "#product_counts{name}"
    const formattedMessage = message.replace('{name}', productId);
    const productCounts = $(formattedMessage).val();
    $.get('/user/shopping-panel?product_id=' + productId + '&count=' + productCounts + '&operation=' + operation);
}

function delete_item_shopping(product_id){
    $.get('/user/delete_item_shopping?product_id=' + product_id);
}