export interface Challenge {
    id: number
    title: string
    description: string
    difficulty: 'Beginner' | 'Intermediate' | 'Advanced'
    points: number
  }