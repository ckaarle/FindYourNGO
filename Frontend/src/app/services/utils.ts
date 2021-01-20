import {NgoFilterSelection, NgoDetailItem, NgoFilterOptions} from '../models/ngo';

export class Utils {

    static clearNullValues(object: any): NgoFilterSelection {
        for (const propName in object) {
            if (object[propName] === null) {
                delete object[propName];
            }
        }
        return object;
    }

    static retrieveObjectKeyFromDisplayName(displayName: string): string {
        let tempFilterObject: NgoFilterOptions = {} as NgoFilterOptions;
        tempFilterObject = this.mapDataToNgoFilterOptions(tempFilterObject);
        let key = 'name';
        for (const entry of Object.entries(tempFilterObject)) {
            if (entry[1].displayName === displayName) {
                key = entry[0];
            }
        }
        return key;
    }

    static mapDataToNgoFilterOptions(ngoOverviewItem: any): NgoFilterOptions {
        // @ts-ignore
        return {
            name: {values: ngoOverviewItem.name},
            branches: {displayName: 'Branches', values: ngoOverviewItem.branches, icon: 'account_tree'},
            regions: {values: ngoOverviewItem.regions},
            topics: {displayName: 'Topics', values: ngoOverviewItem.topics, icon: 'topic'},
            hasEcosoc: {displayName: 'Accreditations', values: ngoOverviewItem.hasEcosoc, icon: 'account_balance'},
            isCredible: {displayName: 'Credibility', values: ngoOverviewItem.isCredible, icon: 'loyalty'},
            countries: {displayName: 'Countries', values: ngoOverviewItem.countries, icon: 'flag'},
            cities: {displayName: 'Cities', values: ngoOverviewItem.cities, icon: 'location_on'},
            contactOptionPresent: {displayName: 'Contactable', values: ngoOverviewItem.contactOptionPresent, icon: 'how_to_reg'},
            typeOfOrganization: {displayName: 'Type of organization', values: ngoOverviewItem.typeOfOrganization, icon: 'corporate_fare'},
            workingLanguages: {displayName: 'Working languages', values: ngoOverviewItem.workingLanguages, icon: 'translate'},
            funding: {displayName: 'Funding', values: ngoOverviewItem.funding, icon: 'attach_money'},
            trustworthiness: {displayName: 'Trustworthiness', values: ngoOverviewItem.trustworthiness, icon: 'star'},
        };
    }

    static mapDataToNgoDetailItem(ngoDetailItem: any): NgoDetailItem {
        return {
            id: ngoDetailItem.id,
            name: ngoDetailItem.name,
            acronym: ngoDetailItem.acronym,
            description: {
                aim: {displayName: 'Description', values: ngoDetailItem.aim},
                typeOfOrganization: {displayName: 'Organization type', values: ngoDetailItem.stats.typeOfOrganization},
                website: {displayName: 'Website', values: ngoDetailItem.contact.website}
            },
            fieldOfActivity: {
                topics: {displayName: 'Topics', values: ngoDetailItem.topics},
                activities: {displayName: 'Activities', values: ngoDetailItem.activities},
                branches: {displayName: 'Branches', values: ngoDetailItem.branches},
                workingLanguages: {displayName: 'Working languages', values: ngoDetailItem.stats.workingLanguages}
            },
            stats: {
                president: {displayName: 'President', values: ngoDetailItem.stats.president},
                foundingYear: {displayName: 'Founding year', values: ngoDetailItem.stats.foundingYear},
                staffNumber: {displayName: 'Staff number', values: ngoDetailItem.stats.staffNumber},
                memberNumber: {displayName: 'Member number', values: ngoDetailItem.stats.memberNumber},
                yearlyIncome: {displayName: 'Yearly income', values: ngoDetailItem.stats.yearlyIncome},
                funding: {displayName: 'Funding', values: ngoDetailItem.stats.funding},
                accreditations: {displayName: 'Accreditations', values: ngoDetailItem.accreditations}
            },
            contact: {
                address: {displayName: 'Address', values: ngoDetailItem.contact.address},
                ngoPhoneNumber: {displayName: 'Phone number', values: ngoDetailItem.contact.ngoPhoneNumber},
                ngoEmail: {displayName: 'Email', values: ngoDetailItem.contact.ngoEmail},
                representative: {displayName: 'Representative', values: ngoDetailItem.contact.representative}
            },
            rating: {
                trustworthiness: {displayName: 'Trustworthiness', values: ngoDetailItem.trustworthiness},
                amount: {displayName: 'Amount', values: ngoDetailItem.amount}
            }
        };
    }
}
