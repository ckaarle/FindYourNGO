export interface TwRating {
  totalTrustworthiness: number;
  baseTrustworthiness: number; // calculated by the system without regard to user comments
  userTrustworthiness: number;
  commentNumberByRating: { [rating: number]: number };
  totalCommentNumber: number;
}
