import language_check
def spellcheck(text):
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    #print(text)
    #print(len(matches)) #this will show the number of errors in the text
    #print(matches[1])   #the number in [] points at the Nth error( 0 <= n < len). remove the [] to see all the errors.
    #print(language_check.correct(text, matches)) #displays corrected textself.
    return {'errorcount':len(matches),'correct':language_check.correct(text, matches)}