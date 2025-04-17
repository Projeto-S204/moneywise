import { test as base } from "@playwright/test"
import { HomePage } from "../page-objects/home_page"
import { LoginPage } from "../page-objects/login_page"


type MyFixtures = {
    homePage: HomePage,
    loginPage: LoginPage
}

export const test = base.extend<MyFixtures> ({
    homePage: async ({ page }, use) => {
        const homePage = new HomePage(page)
        await use(homePage)
    },
    
    loginPage: async ({ page }, use) => {
        const loginPage = new LoginPage(page)
        await use(loginPage)
    }
});