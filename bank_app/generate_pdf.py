import os
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, F
from .models import Account, Transaction


def generatePDF(source_html, output_filename, account_id):
    account = Account.objects.filter(id=str(account_id))
    accountTransactions = Transaction.objects.select_related().filter(
        account_id=str(account_id))
    accountBalance = Account.objects.filter(id=account_id).annotate(
        ammount=Sum('transaction__ammount'))
    data = {
        'account': account,
        'accountBalance': accountBalance,
        'accountTransactions': accountTransactions
    }
    print(data)
    template = get_template(source_html)
    html = template.render(data)

    file = open(output_filename, "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                encoding='utf-8')

    file.close()
    return pisaStatus.err
