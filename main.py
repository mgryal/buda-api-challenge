#import services


def main():
    from services import BudaApiServices, BudaServices
    from utils import from_ddmmyyyyhhmm_to_unix, truncate

    COMISSION_PERCENTAGE = 0.8

    buda_api = BudaApiServices()
    buda_services = BudaServices()
    start_timestamp = from_ddmmyyyyhhmm_to_unix('01/03/2024 13:00')
    end_timestamp = from_ddmmyyyyhhmm_to_unix('01/03/2024 12:00')
    entries = buda_services.get_range_transactions(start_timestamp, end_timestamp)
    buda_entries = list(map(buda_services.from_entry_to_buda_entry, entries))

    lastyear_start_timestamp = from_ddmmyyyyhhmm_to_unix('01/03/2023 13:00')
    lastyear_end_timestamp = from_ddmmyyyyhhmm_to_unix('01/03/2023 12:00')

    lastyear_entries = buda_services.get_range_transactions(lastyear_start_timestamp, lastyear_end_timestamp)
    lastyear_buda_entries = list(map(buda_services.from_entry_to_buda_entry, lastyear_entries))

    traded_money = buda_services.calc_traded_money(buda_entries)

    current_date_transaction = truncate(buda_services.get_btc_transaction_volumen(buda_entries))
    last_year_transaction = truncate(buda_services.get_btc_transaction_volumen(lastyear_buda_entries))
    transaction_percentage_augment = truncate(buda_services.calc_percentage_augment(current_date_transaction, last_year_transaction))
    total_lost_comission = truncate(buda_services.calc_total_lost_comission(traded_money, COMISSION_PERCENTAGE))

    print(f'Traded money: {traded_money} CLP')
    print(f'Transaction volume: {current_date_transaction} BTC')
    print(f'Last year transaction volume: {last_year_transaction} BTC')
    print(f'transaction percentage augment: {transaction_percentage_augment}%')
    print(f'Total lost comission: {total_lost_comission} CLP')

if __name__ == '__main__':
    main()