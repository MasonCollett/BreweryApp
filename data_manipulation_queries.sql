-- Query for add a new character functionality with colon : character being used to 
-- denote the variables that will have data from the backend programming language

-- get all drinks and their information, including secret_ingredient, for browse drinks page
SELECT drinks.id, price, inventory, ingredients.ingredient_name FROM drinks INNER JOIN ingredients ON secret_ingredient = ingredients.id

-- get all promotions and their information for promotions page
SELECT special_promotions.id, discount_percentage, promo_name FROM special_promotions

-- get a single drink's data for the Update People form
SELECT id, price, inventory, secret_ingredient FROM drinks WHERE id = :drink_ID_selected_from_browse_drinks_page

-- get all drinks with their current associated promotions to list
SELECT promo_name, drinks.id AS drink_id
FROM drinks 
INNER JOIN promotions_drinks ON promotions_drinks.drink_id = drinks.id 
INNER JOIN special_promotions on special_promotions.id = promotions_drinks.promotion_id 
ORDER BY drinks.id

-- add a new drink
INSERT INTO drinks (price, inventory, secret_ingredient) VALUES (:priceInput, :inventoryInput, :secret_ingredient_idInput)

-- add a new promotion
INSERT INTO special_promotions (discount_percentage, name) VALUES (:discountInput, :name_Input)

-- associate a drink with a promotion (M-to-M relationship addition)
INSERT INTO promotions_drinks (drink_id, promotion_id) VALUES (:drink_id__Input, :promotion_id_Input)

-- update a drink's data based on submission of the Update Drink form 
UPDATE drinks SET price = :priceInput, inventory = :inventoryInput, secret_ingredient = :secret_ingredient_id_Input WHERE id= :drink_ID_from_the_update_form

-- delete a drink
DELETE FROM drinks WHERE id = :drink_ID_selected_from_browse_drinks_page

-- delete a promotion
DELETE FROM special_promotions WHERE id = :promotion_ID_selected_from_browse_promotions_page

-- dis-associate a promotion from a drink (M-to-M relationship deletion)
DELETE FROM promotions_drinks WHERE drink_id = :drink_ID_selected_from_drink_and_promotion_list AND promotion_id = :promotion_ID_selected_from-drink_and_promotion_list
