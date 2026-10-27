
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";

export default function Home() {
  const locale = useLocale();
  const router = useRouter();
  const t = useTranslations();

  const [apiStatus, setApiStatus] = useState<
    "checking" | "healthy" | "unavailable"
  >("checking");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("API unavailable");
        }
        return response.json();
      })
      .then((data) => {
        setApiStatus(
          data.status === "healthy" ? "healthy" : "unavailable"
        );
      })
      .catch(() => setApiStatus("unavailable"));
  }, []);

  function changeLanguage() {
    const nextLocale = locale === "en" ? "fr" : "en";
    router.replace(`/${nextLocale}`);
  }

  const backendMessage =
    apiStatus === "checking"
      ? t("backendChecking")
      : apiStatus === "healthy"
        ? t("backendHealthy")
        : t("backendUnavailable");

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <Link href={`/${locale}`} className="text-2xl font-bold tracking-tight">
            DocuMind <span className="text-blue-600">AI</span>
          </Link>

          <div className="flex items-center gap-3">
            <button
              onClick={changeLanguage}
              className="rounded-lg border border-slate-200 px-3 py-2 text-sm font-medium hover:bg-slate-100"
              aria-label="Change language"
            >
              {locale === "en" ? "FR" : "EN"}
            </button>

            <span className="hidden text-sm text-slate-500 sm:inline">
              Beta
            </span>
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-6xl px-6 py-16 sm:py-24">
        <div className="mb-8 text-center text-sm">
          {t("backendChecking") === backendMessage &&
          apiStatus === "checking"
            ? "Backend status: "
            : "Backend status: "}

          <span
            className={
              apiStatus === "healthy"
                ? "font-semibold text-green-600"
                : "font-semibold text-amber-600"
            }
          >
            {backendMessage}
          </span>
        </div>

        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-5 inline-flex rounded-full bg-blue-100 px-4 py-2 text-sm font-medium text-blue-700">
            {t("status")}
          </div>

          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            {t("subtitle")}
          </h1>

          <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            {t("description")}
          </p>
        </div>

        <div className="mx-auto mt-14 grid max-w-4xl gap-6 md:grid-cols-2">
          <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-blue-100 text-2xl">
              📄
            </div>

            <h2 className="text-xl font-semibold">{t("upload")}</h2>
            <p className="mt-2 text-sm text-slate-500">
              {t("uploadHint")}
            </p>

            <div className="mt-8 rounded-xl border-2 border-dashed border-slate-300 bg-slate-50 p-8 text-center">
              <span className="text-3xl">⬆️</span>
              <p className="mt-3 text-sm text-slate-600">
                {t("uploadComingSoon")}
              </p>
            </div>
          </section>

          <section className="rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-indigo-100 text-2xl">
              💬
            </div>

            <h2 className="text-xl font-semibold">{t("question")}</h2>
            <p className="mt-2 text-sm leading-6 text-slate-500">
              {t("questionHint")}
            </p>

            <div className="mt-8 rounded-xl border border-slate-200 bg-slate-50 p-5">
              <p className="text-sm text-slate-500">
                {t("askInLanguage")}
              </p>
            </div>

            <button
              disabled
              className="mt-5 w-full cursor-not-allowed rounded-xl bg-blue-600 px-5 py-3 font-medium text-white opacity-50"
            >
              {t("button")}
            </button>
          </section>
        </div>

        <p className="mt-12 text-center text-sm text-slate-500">
          {t("status")}
        </p>
      </section>
    </main>
  );
}
