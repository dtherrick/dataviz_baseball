# from __future__ import division

from bs4 import BeautifulSoup
from datetime import timedelta
from dateutil import parser
import requests


class MLBStandings(object):

    def __init__(self, start='2015-08-01', end='2015-12-31'):
        self._startDate = parser.parse(start)
        self._endDate = parser.parse(end)

        self._url = 'http://www.baseball-reference.com/games/standings.cgi'

        self._masterStandings = []
        self._key = []
        self._header = []

        self.buildMasterStandings()

    @staticmethod
    def daterange(startDate, endDate):
            if startDate == endDate:
                yield startDate
            else:
                for n in range(int((endDate - startDate).days)):
                    yield startDate + timedelta(n)

    def buildPayload(self, currentDate):
        payload = {}
        payload['year'] = currentDate.year
        payload['month'] = currentDate.month
        payload['day'] = currentDate.day
        payload['submit'] = 'Submit+Date'

        return payload

    def getRequest(self, payload):
        r = requests.get(self._url, params=payload)
        if r.ok:
            return r.content
        else:
            raise requests.exceptions.RequestException('Bad Response')

    def getSoup(self, content):
        return BeautifulSoup(content)

    def buildHeaders(self):
        header = []
        master = self._soup('table')[0].findAll(
            'div', {'class': 'table_heading'})
        for element in master:
            if 'Division' in element.string:
                tmp = element.string.rstrip(' Division')
                if tmp not in header:
                    header.append(tmp)
        return header

    def buildKey(self):
        key = []
        for element in self._soup('table')[1].findAll('th'):
            key.append(element.string)
        return key

    def buildStandingsOneDay(self, currentDate):
        dayStandings = []
        for i in range(1, 7):
            B = self._soup('table')[i].findAll('tr')
            for standings in B:
                tmp = {}
                tmp['year'] = currentDate.year
                tmp['month'] = currentDate.month
                tmp['day'] = currentDate.day
                tmp['division'] = self._header[i - 1]
                for j in range(0, len(standings.findAll('td'))):
                    tmp[self._key[j]] = standings.findAll('td')[j].string

                if 'Tm' in tmp.keys():
                    dayStandings.append(tmp)

        return dayStandings

    def buildMasterStandings(self):
        for singleDate in self.daterange(self._startDate, self._endDate):
            payload = self.buildPayload(singleDate)
            content = self.getRequest(payload)
            self._soup = self.getSoup(content)
            self._key = self.buildKey()
            self._header = self.buildHeaders()
            tmpStandings = self.buildStandingsOneDay(singleDate)
            self._masterStandings += tmpStandings

    def getMasterStandings(self):
        return self._masterStandings

if __name__ == '__main__':
    import pandas as pd

    standings = MLBStandings(start='2015-04-05', end='2015-10-04')
    dfMaster = pd.DataFrame(standings.getMasterStandings())
    dfMaster['date'] = pd.to_datetime(
        dfMaster.year.map(str) + '-' +
        dfMaster.month.map(str) + '-' + dfMaster.day.map(str))
    dfMaster.set_index(['division', 'date'], inplace=True)
    dfMaster.drop(['day', 'month', 'year'], axis=1, inplace=True)
    dfMaster.replace({'--': 0}, inplace=True)
    dfMaster['GB'] = dfMaster['GB'].astype(float)

    dfMaster.to_csv('../data/dayByDayStandings2015.csv')
    print 'success'
