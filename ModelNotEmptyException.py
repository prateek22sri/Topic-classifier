class ModelNotEmptyException(Exception):
    message = "Your model is not empty. Create a new model with model type parameter as None and then use load method"
