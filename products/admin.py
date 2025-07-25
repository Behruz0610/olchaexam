from django.contrib import admin
from .models import Category, Product, Comment, ProductImage, Favorite, ProductReview
# ProductReview modelini admin panelga qo'shish
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'review')
# Favorite modelini admin panelga qo'shish
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

# Qo'shimcha rasm modelini alohida ham admin panelga qo'shamiz
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image', 'alt')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'created_at')
    search_fields = ('content',)
