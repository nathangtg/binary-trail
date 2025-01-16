export interface Challenge {
  id: number
  title: string
  description: string
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced'
  category: string
  points: number
  completionRate: number
  tags: string[]
}
