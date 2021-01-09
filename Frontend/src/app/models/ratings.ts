export interface TwRating {
  totalTrustworthiness: number;
  reviewNumberByRating: { [rating: number]: number };
  totalReviewNumber: number;
}

export interface TwReview {
  id: number;
  userId: number;
  userName: string;
  ngoId: number;
  // userProfile: object; TODO?
  reviewsByUser: number;
  created: Date;
  last_edited: Date;
  rating: number;
  text: string;
}

export interface TwReviews {
  reviews: TwReview[];
  reviewNumber: number;
}

export interface NewTwReview {
  reviewId: number;
  ngoId: number;
  userId: number;
  rating: number;
  text: string;
}
