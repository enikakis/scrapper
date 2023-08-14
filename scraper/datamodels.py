from dataclasses import dataclass
from turtle import position


@dataclass
class Institution:
    institution_name: str = None
    website: str = None
    industry: str = None
    type: str = None
    headquarters: str = None
    company_size: int = None
    founded: int = None


@dataclass
class Experience(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    position_title: str = None
    duration: str = None
    location: str = None

    def __repr__(self):
        pos = ""
        if self.position_title:
            pos = "position_title: {position}".format(
                position=self.position_title)
        instt = ""
        if self.institution_name:
            instt = "institution: {institution}".format(
                institution=self.institution_name)
        f_date = ""
        if self.from_date:
            f_date = "fromDate: {from_date}".format(from_date=self.from_date)
        t_date = ""
        if self.to_date:
            t_date = "toDate: {to_date}".format(to_date=self.to_date)
        locat = ""
        if self.location:
            locat = "location: {location}".format(location=self.location)
        return "[{position}, {institution}, {from_date}, {to_date}, {location}]".format(
            position=pos,
            institution=instt,
            from_date=f_date,
            to_date=t_date,
            location=locat)


@dataclass
class Education(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    degree: str = None

    def __repr__(self):
        return "[degree: {degree}, institution: {institution}, fromDate: {from_date}, toDate: {to_date}]".format(
            degree=self.degree,
            institution=self.institution_name,
            from_date=self.from_date,
            to_date=self.to_date
        )


@dataclass
class Accomplishment(Institution):
    title = None
    descriptions = []

    def __repr__(self):
        return "{title}, info: {descriptions}".format(
            title=self.title,
            descriptions=self.descriptions
        )
