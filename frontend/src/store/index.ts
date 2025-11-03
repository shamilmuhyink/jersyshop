import { create } from 'zustand'
import { Product, CartItem, Cart, User } from '@/types'

interface StoreState {
  // User state
  user: User | null
  isAuthenticated: boolean

  // Products state
  products: Product[]
  featuredProducts: Product[]
  selectedProduct: Product | null

  // Cart state
  cart: Cart

  // UI state
  isLoading: boolean
  searchQuery: string
  selectedCategory: string | null

  // Actions
  setUser: (user: User | null) => void
  setAuthenticated: (isAuthenticated: boolean) => void
  setProducts: (products: Product[]) => void
  setFeaturedProducts: (products: Product[]) => void
  setSelectedProduct: (product: Product | null) => void
  setLoading: (isLoading: boolean) => void
  setSearchQuery: (query: string) => void
  setSelectedCategory: (category: string | null) => void

  // Cart actions
  addToCart: (product: Product, size: string, quantity: number) => void
  removeFromCart: (itemId: string) => void
  updateQuantity: (itemId: string, quantity: number) => void
  clearCart: () => void
}

export const useStore = create<StoreState>((set, get) => ({
  // Initial state
  user: null,
  isAuthenticated: false,
  products: [],
  featuredProducts: [],
  selectedProduct: null,
  cart: {
    items: [],
    total: 0,
    itemCount: 0,
  },
  isLoading: false,
  searchQuery: '',
  selectedCategory: null,

  // User actions
  setUser: (user) => set({ user }),
  setAuthenticated: (isAuthenticated) => set({ isAuthenticated }),

  // Product actions
  setProducts: (products) => set({ products }),
  setFeaturedProducts: (featuredProducts) => set({ featuredProducts }),
  setSelectedProduct: (selectedProduct) => set({ selectedProduct }),
  setLoading: (isLoading) => set({ isLoading }),
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  setSelectedCategory: (selectedCategory) => set({ selectedCategory }),

  // Cart actions
  addToCart: (product, size, quantity) => {
    const state = get()
    const variant = product.variants.find(v => v.size === size)

    if (!variant) {
      console.error('Variant not found')
      return
    }

    const existingItemIndex = state.cart.items.findIndex(
      item => item.variant.id === variant.id
    )

    let updatedItems: CartItem[]

    if (existingItemIndex >= 0) {
      // Update existing item
      updatedItems = state.cart.items.map((item, index) =>
        index === existingItemIndex
          ? { ...item, quantity: item.quantity + quantity }
          : item
      )
    } else {
      // Add new item
      const newItem: CartItem = {
        id: `cart-${Date.now()}`,
        product,
        variant,
        quantity,
        addedAt: new Date().toISOString(),
      }
      updatedItems = [...state.cart.items, newItem]
    }

    const total = updatedItems.reduce((sum, item) => {
      const price = item.variant.price || item.product.basePrice
      return sum + (Number(price) * item.quantity)
    }, 0)

    const itemCount = updatedItems.reduce((sum, item) => sum + item.quantity, 0)

    set({
      cart: {
        items: updatedItems,
        total,
        itemCount,
      },
    })

    // Save to localStorage
    localStorage.setItem('cart', JSON.stringify({
      items: updatedItems,
      total,
      itemCount,
    }))
  },

  removeFromCart: (itemId) => {
    const state = get()
    const updatedItems = state.cart.items.filter(item => item.id !== itemId)

    const total = updatedItems.reduce((sum, item) => {
      const price = item.variant.price || item.product.basePrice
      return sum + (Number(price) * item.quantity)
    }, 0)

    const itemCount = updatedItems.reduce((sum, item) => sum + item.quantity, 0)

    set({
      cart: {
        items: updatedItems,
        total,
        itemCount,
      },
    })

    localStorage.setItem('cart', JSON.stringify({
      items: updatedItems,
      total,
      itemCount,
    }))
  },

  updateQuantity: (itemId, quantity) => {
    const state = get()
    const updatedItems = state.cart.items.map(item =>
      item.id === itemId ? { ...item, quantity } : item
    )

    const total = updatedItems.reduce((sum, item) => {
      const price = item.variant.price || item.product.basePrice
      return sum + (Number(price) * item.quantity)
    }, 0)

    const itemCount = updatedItems.reduce((sum, item) => sum + item.quantity, 0)

    set({
      cart: {
        items: updatedItems,
        total,
        itemCount,
      },
    })

    localStorage.setItem('cart', JSON.stringify({
      items: updatedItems,
      total,
      itemCount,
    }))
  },

  clearCart: () => {
    set({
      cart: {
        items: [],
        total: 0,
        itemCount: 0,
      },
    })
    localStorage.removeItem('cart')
  },
}))