import {createI18n} from "vue-i18n";
import {languageStorage} from "@/storage";
import en from "@/i18n/en.json";
import ua from "@/i18n/ua.json";
import ru from "@/i18n/ru.json";


const userLanguage = (localStorage.getItem(languageStorage) || "en");
export default createI18n({
  locale: userLanguage,
  fallbackLocale: "en",
  messages: {
    en: en,
    ru: ru,
    ua: ua
  }
})
