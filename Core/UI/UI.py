class UI:
    def __init__(self, kadoki):
        self.kadoki = kadoki

    def first_launch(self):
        return self.kadoki.settings.first

    def library_list(self):
        return self.kadoki.plugins.libraries()

    def db_list(self):
        return self.kadoki.plugins.dbs()

    # Message to self:
    # I was implementing the drop down lists that
    # go on the first page to login, alongside a button
    # Idea: use a card and center it, logo on top,
    # various options on bottom

