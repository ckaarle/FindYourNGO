export interface TwRating {
  totalTrustworthiness: number;
  reviewNumberByRating: { [rating: number]: number };
  totalReviewNumber: number;
}

export interface TwReview {
  id: number;
  userId: string;
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
  userId: string;
  rating: number;
  text: string;
}

export const EMPTY_TW_REVIEWS: TwReviews = {
  reviews: [],
  reviewNumber: 0
};

export const EMPTY_TW_REVIEW: TwReview = {
  id: 0,
  userId: '',
  userName: '',
  ngoId: 0,
  // userProfile: object; TODO?
  reviewsByUser: 0,
  created: Date.prototype,
  last_edited: Date.prototype,
  rating: 0,
  text: ''
};
