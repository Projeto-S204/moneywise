import type { Locator, Page } from "@playwright/test";

export class TransactionsPage {
  private readonly page: Page;
  private readonly newTransactionBtn: Locator;
  private readonly transactionTitleInput: Locator;
  private readonly paymentMethodSelect: Locator;
  private readonly transactionValueInput: Locator;
  private readonly transactionDateInput: Locator;
  private readonly categorySelect: Locator;
  private readonly transactionDescriptionInput: Locator;
  private readonly transactionCheckbox: Locator;
  private readonly transactionInstallmentsInput: Locator;
  private readonly incomeButton: Locator;
  private readonly expenseButton: Locator;
  private readonly submitButton: Locator;
  private readonly backButton: Locator;

  constructor(page: Page) {
    this.page = page;

    this.newTransactionBtn = page.getByRole('link', { name: 'Nova Transação' });
    this.transactionTitleInput = page.getByRole('textbox', { name: 'Título' });
    this.paymentMethodSelect = page.getByLabel('Método de Pagamento');
    this.transactionValueInput = page.getByRole('textbox', { name: 'Valor' });
    this.transactionDateInput = page.getByRole('textbox', { name: 'Data' });
    this.categorySelect = page.getByLabel('Categoria');
    this.transactionDescriptionInput = page.getByRole('textbox', { name: 'Descrição' });
    this.transactionCheckbox = page.locator('#checkbox');
    this.transactionInstallmentsInput = page.getByRole('spinbutton', { name: 'Número de parcelas' });
    this.expenseButton = page.getByRole('button', { name: ' Despesa' });
    this.submitButton = page.getByRole('button', { name: 'Cadastrar' });
    this.backButton = page.getByText('Voltar');
  }

  async createTransaction(transactionData: any) {
    await this.newTransactionBtn.click();
    await this.transactionTitleInput.fill(transactionData.title);
    await this.paymentMethodSelect.selectOption(transactionData.paymentMethod);
    await this.transactionValueInput.fill(transactionData.value);
    await this.transactionDateInput.fill(transactionData.date);
    await this.categorySelect.selectOption(transactionData.category);
    await this.transactionDescriptionInput.fill(transactionData.description);
    await this.transactionCheckbox.check();
    await this.transactionInstallmentsInput.fill(transactionData.installments);
    await this.page.getByRole('button', { name: transactionData.type }).click();
    await this.submitButton.click();
  }

}