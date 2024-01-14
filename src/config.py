from dotenv import dotenv_values


prod_config = dotenv_values("src/.env_prod")
test_config = dotenv_values("src/.env_test")
