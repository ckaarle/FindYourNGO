import {NgoFilterSelection} from "../models/ngo";

export default class Utils {

    static clearNullValues(object: any): NgoFilterSelection {
        for (const propName in object) {
            if (object[propName] === null) {
                delete object[propName];
            }
        }
        return object;
    }

}