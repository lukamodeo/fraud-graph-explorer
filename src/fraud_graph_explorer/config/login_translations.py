# src/fraud_graph_explorer/config/login_translations.py

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

"""Login page translations (browser language → UI strings)."""

LOGIN_STRINGS = {
    'it': {
        'subtitle': 'Accedi per continuare',
        'username': 'Nome utente',
        'password': 'Password',
        'submit': 'Accedi',
        'error': 'Nome utente o password non validi.',
        'next': 'Effettua il login per accedere a quella pagina.',
    },
    'de': {
        'subtitle': 'Anmelden um fortzufahren',
        'username': 'Benutzername',
        'password': 'Passwort',
        'submit': 'Anmelden',
        'error': 'Ungültiger Benutzername oder Passwort.',
        'next': 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.',
    },
    'fr': {
        'subtitle': 'Connectez-vous pour continuer',
        'username': "Nom d'utilisateur",
        'password': 'Mot de passe',
        'submit': 'Se connecter',
        'error': "Nom d'utilisateur ou mot de passe invalide.",
        'next': 'Veuillez vous connecter pour accéder à cette page.',
    },
    'es': {
        'subtitle': 'Inicie sesión para continuar',
        'username': 'Nombre de usuario',
        'password': 'Contraseña',
        'submit': 'Iniciar sesión',
        'error': 'Nombre de usuario o contraseña no válidos.',
        'next': 'Inicie sesión para acceder a esa página.',
    },
    'en-gb': {
        'subtitle': 'Sign in to continue',
        'username': 'Username',
        'password': 'Password',
        'submit': 'Sign In',
        'error': 'Invalid username or password.',
        'next': 'Please log in to access that page.',
    }
}

# config/login_translations.py

LOCKOUT_STRINGS = {
    "it": {
        "title": "Accesso Temporaneamente Bloccato",
        "icon": "bi-shield-lock",
        "message": "Troppi tentativi di accesso falliti da questo indirizzo IP.",
        "cooldown": "Riprova tra circa 1 ora.",
        "back": "Torna al Login",
    },
    "fr": {
        "title": "Accès Temporairement Bloqué",
        "icon": "bi-shield-lock",
        "message": "Trop de tentatives de connexion échouées depuis cette adresse IP.",
        "cooldown": "Veuillez réessayer dans environ 1 heure.",
        "back": "Retour à la connexion",
    },
    "de": {
        "title": "Zugriff Vorübergehend Gesperrt",
        "icon": "bi-shield-lock",
        "message": "Zu viele fehlgeschlagene Anmeldeversuche von dieser IP-Adresse.",
        "cooldown": "Bitte versuchen Sie es in etwa 1 Stunde erneut.",
        "back": "Zurück zur Anmeldung",
    },
    "es": {
        "title": "Acceso Temporalmente Bloqueado",
        "icon": "bi-shield-lock",
        "message": "Demasiados intentos de inicio de sesión fallidos desde esta dirección IP.",
        "cooldown": "Inténtelo de nuevo en aproximadamente 1 hora.",
        "back": "Volver al inicio de sesión",
    },
    "en": {
        "title": "Access Temporarily Blocked",
        "icon": "bi-shield-lock",
        "message": "Too many failed login attempts from this IP address.",
        "cooldown": "Please try again in approximately 1 hour.",
        "back": "Back to Login",
    },

}