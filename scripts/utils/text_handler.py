import pywikibot

def get_text(page) -> str:
    """
    Get text on page.

    @param page: The page to get text from
    @type page: pywikibot.page.BasePage
    @return: The page's text or None
    """
    try:
        text = page.get()
    except pywikibot.NoPage:
        pywikibot.output(
            "{} doesn't exist, skip!".format(page.title()))
        return None
    except pywikibot.IsRedirectPage:
        pywikibot.output('{} is a redirect, skip!'.format(page.title()))
        return None

    return text


def put_text(page, new: str, summary: str) -> bool:
    """
    Save the new text.
    @param page: The page to update and save
    @type page: pywikibot.page.BasePage
    @param new: The new text for the page
    @param summary: Summary of page changes.
    @return: True if successful, False if unsuccessful, None if
        server error
    """
    page.text = new
    try:
        page.save(summary=summary)
    except pywikibot.EditConflict:
        pywikibot.output('Edit conflict! skip!')
    except pywikibot.ServerError:
            pywikibot.output('Server Error!')
            return None
    except pywikibot.SpamblacklistError as e:
        pywikibot.output(
            'Cannot change {} because of blacklist entry {}'
            .format(page.title(), e.url))
    except pywikibot.LockedPage:
        pywikibot.output('Skipping {} (locked page)'.format(page.title()))
    except pywikibot.PageSaveRelatedError as error:
        pywikibot.output('Error putting page: {}'.format(error.args))
    else:
        return True
    return False