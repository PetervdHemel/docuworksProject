class NoPalindromesError(Exception):
    def __str__(self):
        return f"The processed string contains no palindromes."


class NoEmailAddressesError(Exception):
    def __str__(self):
        return f"The processed string contains no email addresses."