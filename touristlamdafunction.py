import json

def validate_hotel_booking(slots):
    valid_cities = ['phuket','bangkok','pattaya','chiang mai']
    
    if not slots['Location']:
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'Please specify the location where you want to book the hotel.'
        }        
        
    if slots['Location']['value']['originalValue'].lower() not in valid_cities:
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'We currently only support {} as valid destinations.'.format(", ".join(valid_cities))
        }
        
    if not slots['CheckInDate']:
        return {
            'isValid': False,
            'violatedSlot': 'CheckInDate',
            'message': 'Please provide the check-in date.'
        }
        
    if not slots['Nights']:
        return {
            'isValid': False,
            'violatedSlot': 'Nights',
            'message': 'Please specify the number of nights for your stay.'
        }
        
    if not slots['RoomType']:
        return {
            'isValid': False,
            'violatedSlot': 'RoomType',
            'message': 'Please select the type of room you want to book (e.g., king, queen, deluxe).'
        }

    return {'isValid': True}

def validate_tourist_attractions(slots):
    valid_destinations = ['Phuket', 'Bangkok', 'Pattaya', 'Chiang Mai']
    valid_categories = ['Food & Drink', 'Culture', 'Adventure', 'Cultural Experiences']
    valid_durations = ['Half-day', 'Full-day', 'Evening']
    
    if not slots['Destination']:
        return {
            'isValid': False,
            'violatedSlot': 'Destination',
            'message': 'Please specify the destination you want to explore.'
        }
        
    if slots['Destination']['value']['originalValue'].lower() not in valid_destinations:
        return {
            'isValid': False,
            'violatedSlot': 'Destination',
            'message': 'We currently only support {} as valid destinations.'.format(", ".join(valid_destinations))
        }
        
    if not slots['Category']:
        return {
            'isValid': False,
            'violatedSlot': 'Category',
            'message': 'Please select a category for the attractions (e.g., Nature, Culture, Adventure, Entertainment).'
        }
        
    if slots['Category']['value']['originalValue'].lower() not in valid_categories:
        return {
            'isValid': False,
            'violatedSlot': 'Category',
            'message': 'We currently only support {} as valid categories.'.format(", ".join(valid_categories))
        }
        
    if not slots['Duration']:
        return {
            'isValid': False,
            'violatedSlot': 'Duration',
            'message': 'Please specify the duration for exploring attractions (e.g., Half-day, Full-day).'
        }
        
    if slots['Duration']['value']['originalValue'] not in valid_durations:
        return {
            'isValid': False,
            'violatedSlot': 'Duration',
            'message': 'We currently only support {} as valid durations.'.format(", ".join(valid_durations))
        }

    return {'isValid': True}

def validate_transportation(slots):
    valid_modes = ['Bolt', 'Meter Taxi', 'MRT','Grab']
    
    if not slots['OriginLocation']:
        return {
            'isValid': False,
            'violatedSlot': 'OriginLocation',
            'message': 'Could you please provide the starting point for your journey?'
        }
    
    if not slots['DestinationLocation']:
        return {
            'isValid': False,
            'violatedSlot': 'Location',
            'message': 'Please provide the destination for your journey.'
        }
        
    if not slots['Date']:
        return {
            'isValid': False,
            'violatedSlot': 'Date',
            'message': 'When do you plan to travel?'
        }
        
    if not slots['Time']:
        return {
            'isValid': False,
            'violatedSlot': 'Time',
            'message': 'At what time would you like to depart or arrive?'
        }
        
    if not slots['Mode']:
        return {
            'isValid': False,
            'violatedSlot': 'Mode',
            'message': 'Which type of transportation would you like to arrange?'
        }
        
    if slots['Mode']['value']['originalValue'] not in valid_modes:
        return {
            'isValid': False,
            'violatedSlot': 'Mode',
            'message': 'We currently only support {} as valid transportation modes.'.format(", ".join(valid_modes))
        }

    return {'isValid': True}

def lambda_handler(event, context):
    print(json.dumps(event))
    
    intent = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    
    if event['invocationSource'] == 'DialogCodeHook':
        if intent == 'Book a Hotel':
            validation_result = validate_hotel_booking(slots)
        elif intent == 'Explore Tourist Attractions':
            validation_result = validate_tourist_attractions(slots)
        elif intent == 'Arrange Transportation':
            validation_result = validate_transportation(slots)
        else:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Delegate'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
        
        if not validation_result['isValid']:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'ElicitSlot',
                        'slotToElicit': validation_result['violatedSlot']
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots
                    }
                },
                'messages': [{
                    'contentType': 'PlainText',
                    'content': validation_result['message']
                }]
            }
        else:
            return {
                'sessionState': {
                    'dialogAction': {
                        'type': 'Delegate'
                    },
                    'intent': {
                        'name': intent,
                        'slots': slots
                    }
                }
            }
    
    elif event['invocationSource'] == 'FulfillmentCodeHook':
        # Fulfillment logic goes here
        return {
            'sessionState': {
                'dialogAction': {
                    'type': 'Close'
                },
                'intent': {
                    'name': intent,
                    'slots': slots,
                    'state': 'Fulfilled'
                }
            },
            'messages': [{
                'contentType': 'PlainText',
                'content': 'Thanks, your request has been processed.'
            }]
        }
