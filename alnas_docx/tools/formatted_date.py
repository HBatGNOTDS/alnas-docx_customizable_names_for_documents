from datetime import date, datetime

from babel.dates import format_date, format_datetime

LANG = "de_DE"
FORMAT_LANG = "d. MMMM yyyy"
FORMAT_KURZ = "dd.MM.yyyy"
FORMAT_LANG_MIT_ZEIT = "d. MMMM yyyy, HH:mm 'Uhr'"
FORMAT_KURZ_MIT_ZEIT = "dd.MM.yyyy, HH:mm 'Uhr'"
FORMAT_KURZ_MIT_ZEIT_OHNE_KOMMA = "dd.MM.yyyy HH:mm 'Uhr'"
FORMAT_LANG_MIT_ZEIT_UM = "d. MMMM yyyy 'um' HH:mm 'Uhr'"
FORMAT_NUR_UHRZEIT = "HH:mm 'Uhr'"
FORMAT_JAHR = "yyyy"
FORMAT_MONAT = "MMMM"
FORMAT_MONAT_JAHR = "MMMM yyyy"
FORMAT_TAG_MONAT_KURZ = "dd.MM."
FORMAT_TAG_MONAT = "d. MMMM"
FORMAT_QUARTAL = "QQQQ yyyy"
FORMAT_QUARTAL_OHNE_JAHR = "QQQQ"
FORMAT_WOCHENTAG_DATUM = "EEEE, d. MMMM yyyy"
FORMAT_WOCHENTAG_DATUM_MIT_DEN = "EEEE, 'den' d. MMMM yyyy"
FORMAT_WOCHENTAG_DATUM_MIT_ZEIT = "EEEE, d. MMMM yyyy, HH:mm 'Uhr'"
FORMAT_WOCHENTAG_DATUM_MIT_DEN_MIT_ZEIT = "EEEE, 'den' d. MMMM yyyy, HH:mm 'Uhr'"
FORMAT_WOCHENTAG_DATUM_MIT_DEN_UM = "EEEE, 'den' d. MMMM yyyy 'um' HH:mm 'Uhr'"

# Gängige Formate, in denen ein Datum/Datum+Uhrzeit als roher Text ankommen
# kann (z.B. aus Feldern, die intern keinen echten Date-/Datetime-Typ nutzen,
# sondern den Wert nur als Text speichern).
_TEXT_FORMATS = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%d.%m.%Y %H:%M:%S",
    "%d.%m.%Y %H:%M",
    "%Y-%m-%d",
    "%d.%m.%Y",
)


def _parse_text(text):
    """Versucht, rohen Text als Datum oder Datum+Uhrzeit zu interpretieren.
    None, wenn kein bekanntes Format passt."""
    if not text:
        return None
    for fmt in _TEXT_FORMATS:
        try:
            return datetime.strptime(text.strip(), fmt)
        except ValueError:
            continue
    return None


class _DateComponentsMixin:
    """Eigenschaften, die sich für FormattedDate und FormattedDateTime
    identisch verhalten - betreffen nur den Datumsanteil (nie die Uhrzeit)
    und sind deshalb für beide Feldtypen gleich richtig."""

    @property
    def jahr(self):
        return format_date(self, format=FORMAT_JAHR, locale=LANG)

    @property
    def monat(self):
        return format_date(self, format=FORMAT_MONAT, locale=LANG)

    @property
    def monat_jahr(self):
        return format_date(self, format=FORMAT_MONAT_JAHR, locale=LANG)

    @property
    def tag_monat_kurz(self):
        return format_date(self, format=FORMAT_TAG_MONAT_KURZ, locale=LANG)

    @property
    def tag_monat(self):
        return format_date(self, format=FORMAT_TAG_MONAT, locale=LANG)

    @property
    def quartal(self):
        return format_date(self, format=FORMAT_QUARTAL, locale=LANG)

    @property
    def quartal_ohne_jahr(self):
        return format_date(self, format=FORMAT_QUARTAL_OHNE_JAHR, locale=LANG)

    @property
    def wochentag_datum(self):
        return format_date(self, format=FORMAT_WOCHENTAG_DATUM, locale=LANG)

    @property
    def wochentag_datum_mit_den(self):
        return format_date(self, format=FORMAT_WOCHENTAG_DATUM_MIT_DEN, locale=LANG)


class FormattedDate(_DateComponentsMixin, date):
    """Verhält sich wie ein normales date-Objekt (Vergleiche, Rechenoperationen,
    Übergabe an formatdate() funktionieren unverändert). Standard ist immer
    reines Datum, ohne Uhrzeit - bei einem echten Datum-Feld gibt es ja auch
    keine.

    Die '..._mit_zeit'-Eigenschaften existieren hier als Rückfall-Varianten:
    falls jemand aus Versehen eine Zeit-Eigenschaft auf einem reinen
    Datumsfeld aufruft (weil nicht immer auf den ersten Blick klar ist, ob
    ein Feld eine Uhrzeit hat), kommt die datumslose Fassung zurück statt
    eines Fehlers oder eines falschen 'False' im Fließtext. Nur .uhrzeit hat
    dafür keine sinnvolle Entsprechung und liefert einen leeren Text."""

    def __str__(self):
        return format_date(self, format=FORMAT_LANG, locale=LANG)

    @property
    def kurz(self):
        return format_date(self, format=FORMAT_KURZ, locale=LANG)

    @property
    def kurz_mit_zeit(self):
        return self.kurz

    @property
    def lang_mit_zeit(self):
        return str(self)

    @property
    def kurz_mit_zeit_ohne_komma(self):
        return self.kurz

    @property
    def lang_mit_zeit_um(self):
        return str(self)

    @property
    def uhrzeit(self):
        return ""

    @property
    def wochentag_datum_mit_zeit(self):
        return self.wochentag_datum

    @property
    def wochentag_datum_mit_den_mit_zeit(self):
        return self.wochentag_datum_mit_den

    @property
    def wochentag_datum_mit_den_um(self):
        return self.wochentag_datum_mit_den


class FormattedDateTime(_DateComponentsMixin, datetime):
    """Wie FormattedDate, für Werte mit echter Uhrzeit. Standard ist
    ebenfalls reines Datum (einheitlich mit FormattedDate) - die Uhrzeit
    kommt nur über eine der '..._mit_zeit'-Eigenschaften dazu."""

    def __str__(self):
        return format_date(self, format=FORMAT_LANG, locale=LANG)

    @property
    def kurz(self):
        return format_date(self, format=FORMAT_KURZ, locale=LANG)

    @property
    def kurz_mit_zeit(self):
        return format_datetime(self, format=FORMAT_KURZ_MIT_ZEIT, locale=LANG)

    @property
    def lang_mit_zeit(self):
        return format_datetime(self, format=FORMAT_LANG_MIT_ZEIT, locale=LANG)

    @property
    def kurz_mit_zeit_ohne_komma(self):
        return format_datetime(self, format=FORMAT_KURZ_MIT_ZEIT_OHNE_KOMMA, locale=LANG)

    @property
    def lang_mit_zeit_um(self):
        return format_datetime(self, format=FORMAT_LANG_MIT_ZEIT_UM, locale=LANG)

    @property
    def uhrzeit(self):
        return format_datetime(self, format=FORMAT_NUR_UHRZEIT, locale=LANG)

    @property
    def wochentag_datum_mit_zeit(self):
        return format_datetime(self, format=FORMAT_WOCHENTAG_DATUM_MIT_ZEIT, locale=LANG)

    @property
    def wochentag_datum_mit_den_mit_zeit(self):
        return format_datetime(self, format=FORMAT_WOCHENTAG_DATUM_MIT_DEN_MIT_ZEIT, locale=LANG)

    @property
    def wochentag_datum_mit_den_um(self):
        return format_datetime(self, format=FORMAT_WOCHENTAG_DATUM_MIT_DEN_UM, locale=LANG)


def datum(value):
    """Verpackt einen Datums-/Datum+Uhrzeit-Wert in FormattedDate/
    FormattedDateTime, damit in der Word-Vorlage zusätzliche Eigenschaften
    wie .kurz, .monat_jahr, .wochentag_datum usw. zur Verfügung stehen.
    Standard (ohne Attribut) ist immer reines Datum, Uhrzeit nur über ein
    '..._mit_zeit'-Attribut.

    Akzeptiert: ein echtes date-Objekt, ein echtes datetime-Objekt, oder
    rohen Text (für Felder, die Datum/Zeit nur als Text speichern - wird
    automatisch geparst). Leere/nicht erkennbare Werte geben den
    Eingabewert unverändert zurück, damit {% if datum(...) %} weiterhin
    funktioniert, statt einen Fehler zu werfen."""
    if isinstance(value, datetime):
        return FormattedDateTime(
            value.year, value.month, value.day,
            value.hour, value.minute, value.second,
        )
    if isinstance(value, date):
        return FormattedDate(value.year, value.month, value.day)
    if isinstance(value, str):
        parsed = _parse_text(value)
        if parsed is None:
            return value
        if ":" in value:
            return FormattedDateTime(
                parsed.year, parsed.month, parsed.day,
                parsed.hour, parsed.minute, parsed.second,
            )
        return FormattedDate(parsed.year, parsed.month, parsed.day)
    return value
