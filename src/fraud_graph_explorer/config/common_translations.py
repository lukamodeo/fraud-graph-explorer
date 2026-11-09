# src/fraud_graph_explorer/config/common_translations.py

# Fraud Graph Explorer
# Copyright (C) 2026 Luca Amodeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Common page translations (browser language → UI strings)."""

COMMON_STRINGS = {
    "it": {
        # --- Login page ---
        "LOGIN_SUBTITLE":   "Accedi per continuare",
        "LOGIN_USERNAME":   "Nome utente",
        "LOGIN_PASSWORD":   "Password",
        "LOGIN_SUBMIT":     "Accedi",
        "LOGIN_ERROR":      "Nome utente o password non validi.",
        # --- Lockout page ---
        "LOCKOUT_TITLE":    "Accesso Temporaneamente Bloccato",
        "LOCKOUT_ICON":     "bi-shield-lock",
        "LOCKOUT_MESSAGE":  "Troppi tentativi di accesso falliti da questo indirizzo IP.",
        "LOCKOUT_COOLDOWN": "Riprova tra circa 1 ora.",
        "LOCKOUT_BACK":     "Torna al Login",
        # --- Screen resolution warning ---
        "SCREEN_TOO_SMALL": "Schermo troppo piccolo",
        "SCREEN_SMALL_TIP": "Questa applicazione richiede una larghezza minima dello schermo di 1280 px.<br>Utilizza un computer o un tablet in modalità orizzontale con uno schermo più grande.",
    },
    "de": {
        # --- Login page ---
        "LOGIN_SUBTITLE":   "Anmelden um fortzufahren",
        "LOGIN_USERNAME":   "Benutzername",
        "LOGIN_PASSWORD":   "Passwort",
        "LOGIN_SUBMIT":     "Anmelden",
        "LOGIN_ERROR":      "Ungültiger Benutzername oder Passwort.",
        # --- Lockout page ---
        "LOCKOUT_TITLE":    "Zugriff Vorübergehend Gesperrt",
        "LOCKOUT_ICON":     "bi-shield-lock",
        "LOCKOUT_MESSAGE":  "Zu viele fehlgeschlagene Anmeldeversuche von dieser IP-Adresse.",
        "LOCKOUT_COOLDOWN": "Bitte versuchen Sie es in etwa 1 Stunde erneut.",
        "LOCKOUT_BACK":     "Zurück zur Anmeldung",
        # --- Screen resolution warning ---
        "SCREEN_TOO_SMALL": "Bildschirm zu klein",
        "SCREEN_SMALL_TIP": "Diese Anwendung erfordert eine Mindestbildschirmbreite von 1280 px.<br>Bitte verwende einen Desktop-Computer oder ein Tablet im Querformat mit einem größeren Bildschirm.",
    },
    "fr": {
        # --- Login page ---
        "LOGIN_SUBTITLE":   "Connectez-vous pour continuer",
        "LOGIN_USERNAME":   "Nom d'utilisateur",
        "LOGIN_PASSWORD":   "Mot de passe",
        "LOGIN_SUBMIT":     "Se connecter",
        "LOGIN_ERROR":      "Nom d'utilisateur ou mot de passe invalide.",
        # --- Lockout page ---
        "LOCKOUT_TITLE":    "Accès Temporairement Bloqué",
        "LOCKOUT_ICON":     "bi-shield-lock",
        "LOCKOUT_MESSAGE":  "Trop de tentatives de connexion échouées depuis cette adresse IP.",
        "LOCKOUT_COOLDOWN": "Veuillez réessayer dans environ 1 heure.",
        "LOCKOUT_BACK":     "Retour à la connexion",
        # --- Screen resolution warning ---
        "SCREEN_TOO_SMALL": "Écran trop petit",
        "SCREEN_SMALL_TIP": "Cette application nécessite une largeur d’écran minimale de 1280 px.<br>Veuillez utiliser un ordinateur ou une tablette en mode paysage avec un écran plus large.",
    },
    "es": {
        # --- Login page ---
        "LOGIN_SUBTITLE":   "Inicie sesión para continuar",
        "LOGIN_USERNAME":   "Nombre de usuario",
        "LOGIN_PASSWORD":   "Contraseña",
        "LOGIN_SUBMIT":     "Iniciar sesión",
        "LOGIN_ERROR":      "Nombre de usuario o contraseña no válidos.",
        # --- Lockout page ---
        "LOCKOUT_TITLE":    "Acceso Temporalmente Bloqueado",
        "LOCKOUT_ICON":     "bi-shield-lock",
        "LOCKOUT_MESSAGE":  "Demasiados intentos de inicio de sesión fallidos desde esta dirección IP.",
        "LOCKOUT_COOLDOWN": "Inténtelo de nuevo en aproximadamente 1 hora.",
        "LOCKOUT_BACK":     "Volver al inicio de sesión",
        # --- Screen resolution warning ---
        "SCREEN_TOO_SMALL": "Pantalla demasiado pequeña",
        "SCREEN_SMALL_TIP": "Esta aplicación requiere un ancho de pantalla mínimo de 1280 px.<br>Utiliza un ordenador o una tableta en modo horizontal con una pantalla más grande.",
    },
    "en-gb": {
        # --- Login page ---
        "LOGIN_SUBTITLE":   "Sign in to continue",
        "LOGIN_USERNAME":   "Username",
        "LOGIN_PASSWORD":   "Password",
        "LOGIN_SUBMIT":     "Sign In",
        "LOGIN_ERROR":      "Invalid username or password.",
        # --- Lockout page ---
        "LOCKOUT_TITLE":    "Access Temporarily Blocked",
        "LOCKOUT_ICON":     "bi-shield-lock",
        "LOCKOUT_MESSAGE":  "Too many failed login attempts from this IP address.",
        "LOCKOUT_COOLDOWN": "Please try again in approximately 1 hour.",
        "LOCKOUT_BACK":     "Back to Login",
        # --- Screen resolution warning ---
        "SCREEN_TOO_SMALL": "Screen too small",
        "SCREEN_SMALL_TIP": "This application requires a minimum screen width of 1280 px.<br>Please use a desktop computer or a tablet in landscape mode with a larger display."
    }
}
