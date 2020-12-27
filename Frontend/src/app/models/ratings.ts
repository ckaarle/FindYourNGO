export interface TwRating {
  totalTrustworthiness: number;
  baseTrustworthiness: number; // calculated by the system with no regard to user comments
  userTrustworthiness: number;
  commentNumberByRating: { [rating: number]: number };
  totalCommentNumber: number;
}

export interface TwComment {
  id: number;
  userId: number;
  userName: string;
  ngoId: number;
  // userProfile: object; TODO?
  commentsByUser: number;
  created: Date;
  last_edited: Date;
  rating: number;
  text: string;
}

export interface TwComments {
  comments: TwComment[];
  commentNumber: number;
}

export interface NewTwComment {
  commentId: number;
  ngoId: number;
  userId: number;
  rating: number;
  text: string;
}
