export interface TwRating {
  totalTrustworthiness: number;
  baseTrustworthiness: number; // calculated by the system with no regard to user comments
  userTrustworthiness: number;
  commentNumberByRating: { [rating: number]: number };
  totalCommentNumber: number;
}

export interface TwComment {
  userName: string;
  userProfile: undefined; // TODO?
  created: Date;
  last_edited: Date;
  rating: number;
  text: string;
}

export interface TwComments {
  ownComment: TwComment | undefined;
  otherComments: TwComment[];
  commentNumber: number;
}
