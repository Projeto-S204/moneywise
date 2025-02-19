import datetime

def convert_value(transaction_data):
    update_fields = []
    update_values = []

    for key, value in transaction_data.items():
        if key == "transaction_id":
            continue

        if value == "":
            value = None

        if key == 'is_recurring' and value is None:
            value = False
            transaction_data['start_date'] = None
            transaction_data['end_date'] = None
            transaction_data['interval'] = None
            transaction_data['number_of_payments'] = None

        if key == 'number_of_payments':
            if value is not None:
                value = int(value)

        if key == 'amount' and value is not None:
            value = float(value)

        if key == 'transaction_date' and value is not None:
            value = datetime.datetime.strptime(value, '%Y-%m-%d').date()

        if key == 'transaction_hour' and value is not None:
            value = datetime.datetime.strptime(value, '%H:%M').time()

        update_fields.append(f"{key} = %s")
        update_values.append(value)

    update_values.append(transaction_data['transaction_id'])

    return update_fields, update_values