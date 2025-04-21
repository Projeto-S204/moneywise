import { test as base } from "@playwright/test"
import { BaseSetup } from "../page-objects/base_setup"
import { HomePage } from "../page-objects/home_page"
import { SigninPage } from "../page-objects/signin_page"
import { SignupPage } from "../page-objects/signup_page"
import { TransactionsPage } from "../page-objects/transactions_page"

import dotenv from 'dotenv';
dotenv.config();

const URL = 'http://127.0.0.1:' + process.env.AVAILABLE_PORT;


type MyFixtures = {
    baseSetup: BaseSetup,
    homePage: HomePage,
    signinPage: SigninPage,
    signupPage: SignupPage,
    transactionsPage: TransactionsPage
}

export const test = base.extend<MyFixtures>({
    baseSetup: async ({ page }, use) => {
        const baseSetup = new BaseSetup(page);
        await use(baseSetup);
    },

    homePage: async ({ baseSetup }, use) => {
        await baseSetup.goto(URL);
        const homePage = new HomePage(baseSetup.getPage());
        await use(homePage);
    },

    signinPage: async ({ homePage }, use) => {
        await homePage.gotoSigninPage();
        const signinPage = new SigninPage(homePage.getPage());
        await use(signinPage);
    },

    signupPage: async ({ homePage }, use) => {
        await homePage.gotoSignupPage();
        const signupPage = new SignupPage(homePage.getPage());
        await use(signupPage);
    },

    transactionsPage: async ({ signinPage }, use) => {
        await signinPage.login('test@test.com', '12345678')
        const transactionsPage = new TransactionsPage(signinPage.getPage());
        await use(transactionsPage);
    }
});