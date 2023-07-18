
$(document).ready(function() {

    // Add to Cart button click event
    $(document).on('click', '.add-to-cart-button', function(e) {
        e.preventDefault();
        
        
        const productID = $(this).data('product-id');
        const productQuantity = $('#product-quantity').val();

        console.log(productQuantity)
        
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
                quantity: productQuantity
            },
            success: function(response) {
                if (response.success) {
                    $('#basket-quantity').text(response.basket_quantity);
                    $('#basket-total-price').text('£' + response.basket_total_price);
                    $('#basket-total-price2').text('£' + response.basket_total_price);
                    
                    // Update the product list in the navbar
                    var productList = response.product_list;
                    var $minicartProductList = $('.minicart-product-list');
                    $minicartProductList.empty();
                    productList.forEach(function(product) {
                        var productHtml = '<li>' +
                            '<a href=" ' + product.url + ' " class="minicart-product-image">' +
                            '<img src="' + product.picture + '" alt="cart products">' +
                            '</a>' +
                            '<div class="minicart-product-details">' +
                            '<h6><a href="'+ product.url +'">' + product.name + '</a></h6>' +
                            '<span>£' + product.unit_price + ' x ' + product.quantity + '</span>' +
                            '</div>' +
                            '<button class="close remove-from-cart-button" data-product-id="' + product.id + '" title="Remove">' +
                            '<i class="fa fa-close"></i>' +
                            '</button>' +
                            '</li>';
                        $minicartProductList.append(productHtml);
                    });
                    alert(response.message);
                } else {
                    alert('Failed to add the product to the cart.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });






    // Remove from cart click event
    $('.minicart-product-list').on('click', '.remove-from-cart-button', function(e) {
        e.preventDefault();
        console.log("asdfghjklkjhgfdsasdfghj")

        const productID = $(this).data('product-id');
        console.log(productID)

        
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_cart/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                if (response.success) {
                    $('#basket-quantity').text(response.basket_quantity);
                    $('#basket-total-price').text('£' + response.basket_total_price);
                    $('#basket-total-price2').text('£' + response.basket_total_price);
                    
                    // Update the product list in the navbar
                    var productList = response.product_list;
                    var $minicartProductList = $('.minicart-product-list');
                    $minicartProductList.empty();
                    productList.forEach(function(product) {
                        var productHtml = '<li>' +
                            '<a href=" ' + product.url + ' " class="minicart-product-image">' +
                            '<img src="' + product.picture + '" alt="cart products">' +
                            '</a>' +
                            '<div class="minicart-product-details">' +
                            '<h6><a href="'+ product.url +'">' + product.name + '</a></h6>' +
                            '<span>£' + product.unit_price + ' x ' + product.quantity + '</span>' +
                            '</div>' +
                            '<button class="close remove-from-cart-button" data-product-id="' + product.id + '" title="Remove">' +
                            '<i class="fa fa-close"></i>' +
                            '</button>' +
                            '</li>';
                        $minicartProductList.append(productHtml);
                    });
                    alert(response.message);
                } else {
                    alert('Failed to delete the product from the cart.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });




    $(document).on('click', '.add-to-wishlist-button', function(e) {
        e.preventDefault();

        const productID = $(this).data('product-id');
        console.log(productID)
        
        $.ajax({
            type: 'POST',
            url: productID + "/add_to_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                if (response.success) {
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    alert(response.message);
                } else {
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });




    $('.remove-from-wishlist-button').click(function(e) {
        e.preventDefault();
        console.log("wishlist+++++++++++++++++++++++")

        const productID = $(this).data('product-id');
        console.log(productID)
        
        $.ajax({
            type: 'POST',
            url: productID + "/remove_from_wishlist/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                product_id: productID,
            },
            success: function(response) {
                if (response.success) {
                    // Update the wishlist information in navbar
                    $('#wishlist-quantity').text(response.wishlist_quantity);

                    $(e.target).closest('tr').remove();

                    alert(response.message);
                } else {
                    alert('Failed to add the product to the wishlist.');
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });


  

    $('.subscribe-btn').click(function(e) {
        e.preventDefault();

        const subscribeForm = document.getElementById('subscribe-form');
        const emailInput = document.getElementById('mc-email').value;
        
        $.ajax({
            type: 'POST',
            url:"/subscribe/",
            data: {
                csrfmiddlewaretoken: csrftoken,
                emailInput: emailInput,
            },
            success: function(response) {
                if (response.success) {
                    alert('Subscription successful!');
                } else {
                    alert('Subscription failed. ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    });







    const categoryIdElement = document.getElementById('category-id');
    const categoryId = categoryIdElement.innerText;
    console.log(categoryId)
    let sortByOption = 'trending';

    $('.btn-clear-all').on('click', function() {
        $('input[type="checkbox"]').prop('checked', false);
        
        $('.nice-select').val('trending').niceSelect('update');
        
        applyFilters();
    });
        
    $('.filter-option').on('click', function() {
        applyFilters();
    });

    $('.nice-select').on('change', function() {
        sortByOption = $(this).val();
        console.log(sortByOption);
        applyFilters();
    });

    function applyFilters() {
        var selectedBrands = [];
        var selectedSizes = [];
        var selectedColors = [];

        $('input[name="brand"]:checked').each(function() {
            selectedBrands.push($(this).val());
        });

        $('input[name="size"]:checked').each(function() {
            selectedSizes.push($(this).val());
        });

        $('input[name="color"]:checked').each(function() {
            selectedColors.push($(this).val());
        });

        $.ajax({
            type: 'POST',
            url: 'apply_filters/',
            data: {
                'brands': selectedBrands,
                'sizes': selectedSizes,
                'colors': selectedColors,
                'sort_by': sortByOption, 
                csrfmiddlewaretoken: csrftoken,
            },
            dataType: 'json',
            success: function(response) {
                if (response.success) {
                    $('#product-count').text(response.product_count);
                    
                    var productList = response.products;
                    const productContainer = document.getElementById("search-product-list");
                    productContainer.innerHTML = "";

                    response.products.forEach(product => {
                        productContainer.innerHTML += `
                        <div class="col-lg-4 col-md-4 col-sm-6 mt-40">
                            <div class="single-product-wrap">
                                <div id="product-id" hidden>${product.id}</div>
                                <div class="product-image">
                                    <a href="${product.url}">
                                    <img src="${product.picture}" alt="Li's Product Image">
                                    </a>
                                    <span class="sticker">New</span>
                                </div>
                                <div class="product_desc">
                                    <div class="product_desc_info">
                                    <div class="product-review">
                                        <div class="rating-box">
                                        <ul class="rating">
                                            <li><i class="fa fa-star-o"></i></li>
                                            <li><i class="fa fa-star-o"></i></li>
                                            <li><i class="fa fa-star-o"></i></li>
                                            <li class="no-star"><i class="fa fa-star-o"></i></li>
                                            <li class="no-star"><i class="fa fa-star-o"></i></li>
                                        </ul>
                                        </div>
                                    </div>
                                    <h4><a class="product_name" href="${product.url}">${product.name}</a></h4>
                                    <div class="price-box">
                                        <span class="new-price new-price-2">$ ${ product.price } </span>
                                    </div>
                                    </div>
                                    <div class="add-actions">
                                    <ul class="add-actions-link">
                                        <li class="add-cart active"><a href="#" class="add-to-cart-button" data-product-id="${product.id}">Add to cart</a></li>
                                        <li><a class="links-details add-to-wishlist-button" href="#" data-product-id="${product.id}"><i class="fa fa-heart-o"></i></a></li>
                                        <li><a href="#" title="quick view" class="quick-view-btn" data-toggle="modal" data-target="#exampleModalCenter"><i class="fa fa-eye"></i></a></li>
                                    </ul>
                                    </div>
                                </div>
                                </div>
                        </div>`;
                    });
                    console.log(response.message);
                } else {
                    console.log('Failed to filter products.');
                }
            },
            error: function() {
                // Ajax fail
            }
        });
    }
});



