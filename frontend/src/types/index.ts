// User related types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  isActive: boolean;
  isAdmin: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
}

// Product related types
export interface Product {
  id: string;
  name: string;
  slug: string;
  description?: string;
  team: string;
  player?: string;
  sport: string;
  brand?: string;
  basePrice: number;
  salePrice?: number;
  material?: string;
  careInstructions?: string;
  averageRating?: number;
  reviewCount: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
  variants: ProductVariant[];
}

export interface ProductVariant {
  id: string;
  productId: string;
  size: string;
  color?: string;
  sku: string;
  stockQuantity: number;
  price?: number;
  imageUrls: string[];
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  sport: string;
}

export interface ProductFilters {
  sport?: string;
  team?: string[];
  size?: string[];
  minPrice?: number;
  maxPrice?: number;
  brand?: string[];
  sortBy?: 'price_asc' | 'price_desc' | 'newest' | 'popular' | 'rating';
}

// Cart related types
export interface CartItem {
  id: string;
  product: Product;
  variant: ProductVariant;
  quantity: number;
  addedAt: string;
}

export interface Cart {
  items: CartItem[];
  total: number;
  itemCount: number;
}

// Order related types
export interface Order {
  id: string;
  orderNumber: string;
  userId?: string;
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  subtotal: number;
  taxAmount: number;
  shippingAmount: number;
  totalAmount: number;
  shippingAddress: Address;
  billingAddress?: Address;
  paymentMethod: string;
  paymentStatus: string;
  trackingNumber?: string;
  notes?: string;
  items: OrderItem[];
  createdAt: string;
  updatedAt: string;
}

export interface OrderItem {
  id: string;
  productId: string;
  productName: string;
  productImage: string;
  size: string;
  color?: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
}

export interface Address {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}